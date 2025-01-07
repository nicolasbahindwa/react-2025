from typing import Optional, Generic, TypeVar
from uuid import UUID
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User
from app.schemas.user import UserCreate, UserUpdate, UserPatch, UserResponse
from app.repositories.base import BaseRepository
from app.exceptions.database import (
    DatabaseError, 
    InvalidFieldException, 
    InvalidDataException,
    DatabaseCommitException,
    UpdateFailedException,
    NotFoundException,
    EmailSendError
)
from sqlalchemy import select
from app.models.email import EmailTemplate
from app.services.email import EmailService
from app.core.logging import app_logger, log_operation
from app.utils.emailSettings import get_email_settings
from app.config.email import EmailConfig
from app.database.session import managed_transaction

# Type variables for generic type hints
ModelType = TypeVar("ModelType", bound=User)
CreateSchemaType = TypeVar("CreateSchemaType", bound=UserCreate)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=UserUpdate)
PatchSchemaType = TypeVar("PatchSchemaType", bound=UserPatch)

class UserRepository(
    BaseRepository[User, UserCreate, UserUpdate, UserPatch],
    Generic[ModelType, CreateSchemaType, UpdateSchemaType, PatchSchemaType]
):
    """
    User Repository with enhanced functionality for user management
    """
    def __init__(self, db: AsyncSession):
        """
        Initialize UserRepository with database session
        
        Args:
            db: AsyncSession - The database session to use
        """
        super().__init__(User, db)
        self._settings = get_email_settings()
        self._email_config = EmailConfig()
        self._email_service = EmailService()
    
    async def get_current_user(self, token: str) -> User:
        """Retrieve the current authenticated user based on the access token."""
        try:
            # Decode and validate the token
            payload = self.jwt_handler.decode_token(token)
            user_id = payload.get("sub")
            
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: Missing user ID",
                )

            # Query the database for the user
            user = await self._session.scalar(
                select(User).where(User.id == user_id)
            )
            
            if not user:
                raise NotFoundException("User not found")
            
            return user
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )

    async def create(
        self, 
        schema: CreateSchemaType, 
        client_ip: str,
        custom_activation_url: Optional[str] = None
    ) -> UserResponse:
        """
        Create user with enhanced error handling for unique constraints
        """
        context = self._log_context("create")
        token = None

        async with managed_transaction() as db:
            try:
                # Create user instance
                db_obj = User(
                    username=schema.username,
                    email=str(schema.email),
                    is_active=False,
                    last_login_ip=client_ip
                )
                db_obj.set_password(schema.password)
                
                # Add to session and flush to generate ID
                db.add(db_obj)
                app_logger.log_success("Added user to session")
                await db.flush()
                app_logger.log_success("Flushed user to session")
                
                # Handle activation token and email
                if not db_obj.is_active:
                    token = await db_obj.create_activation_token(db)
                    if token:
                        await self._send_activation_email(
                            db_obj, 
                            token.token, 
                            custom_activation_url
                        )
                        app_logger.log_success("Sent activation email")

                await db.refresh(db_obj)
                
                app_logger.log_success(
                    "User created successfully", 
                    extra={
                        **context,
                        "user_id": str(db_obj.id),
                        "username": db_obj.username
                    }
                )
                
                return db_obj

            except IntegrityError as e:
                await self._handle_integrity_error(e)

            except EmailSendError as e:
                self._log_email_error(e, db_obj, context)
                raise

            except SQLAlchemyError as e:
                self._log_database_error("Database error during user creation", e, context)
                raise DatabaseCommitException(f"Failed to commit user creation: {str(e)}")

            except Exception as e:
                self._log_database_error("Unexpected error during user creation", e, context)
                raise DatabaseError(f"Error creating user: {str(e)}")



    async def update(
        self, 
        *, 
        id: UUID, 
        schema: UpdateSchemaType, 
        auto_commit: bool = True
    ) -> ModelType:
        """
        Update user with enhanced error handling
        
        Args:
            id: User ID
            schema: Update schema with new data
            auto_commit: Whether to commit changes immediately
            
        Returns:
            ModelType: Updated user
            
        Raises:
            NotFoundException: If user not found
            InvalidFieldException: If invalid field in update data
            InvalidDataException: If unique constraint violated
            UpdateFailedException: For other update errors
        """
        context = self._log_context("update", id=str(id))
        
        user = await self.get_by_id(id)
        if not user:
            raise NotFoundException("User", id)
        async with managed_transaction() as db:
            try:
                # Handle password update
                if schema.password:
                    user.set_password(schema.password)
                
                # Update other fields
                update_data = schema.model_dump(exclude={'password'}, exclude_unset=True)
                await self._update_fields(user, update_data)
                
                # Commit changes if requested
                if auto_commit:
                    await db.commit()
                    await db.refresh(user)
                
                app_logger.log_success(
                    f"Successfully updated user {user.username}",
                    extra=context
                )
                return user

            except IntegrityError as e:
                await self._handle_integrity_error(e)

            except SQLAlchemyError as e:
                self._log_database_error("Failed to update user", e, context)
                raise UpdateFailedException(f"Failed to update user: {str(e)}")


    async def patch(
        self, 
        *, 
        id: UUID, 
        schema: PatchSchemaType, 
        auto_commit: bool = True
    ) -> ModelType:
        """
        Partially update user with enhanced error handling
        
        Args:
            id: User ID
            schema: Patch schema with partial update data
            auto_commit: Whether to commit changes immediately
            
        Returns:
            ModelType: Updated user
            
        Raises:
            NotFoundException: If user not found
            InvalidFieldException: If invalid field in patch data
            InvalidDataException: If unique constraint violated
            UpdateFailedException: For other update errors
        """
        context = self._log_context("patch", id=str(id))

        user = await self.get_by_id(id)
        if not user:
            raise NotFoundException("User", id)

        async with managed_transaction() as db:
            try:
                # Handle password update
                patch_data = schema.model_dump(exclude_unset=True, exclude_none=True)
                if patch_data.get('password'):
                    user.set_password(patch_data.pop('password'))
                
                # Update other fields
                await self._update_fields(user, patch_data)
                
                # Commit changes if requested
                if auto_commit:
                    await db.commit()
                    await db.refresh(user)
                
                app_logger.log_success(
                    f"Successfully patched user {user.username}",
                    extra=context
                )
                return user

            except IntegrityError as e:
                await self._handle_integrity_error(e)

            except SQLAlchemyError as e:
                self._log_database_error("Failed to patch user", e, context)
                raise UpdateFailedException(f"Failed to patch user: {str(e)}")

 

    @log_operation("delete_user_account")
    async def delete_account(self, id: UUID) -> None:
        """
        Delete a user account.

        Args:
            id: The user ID of the account to be deleted.

        Raises:
            NotFoundException: If the user does not exist.
            DatabaseError: If there's a database error.
        """
        context = self._log_context("delete", id=str(id))
        
        user = await self.get_by_id(id)
        if not user:
            raise NotFoundException("User", id)
        
        async with managed_transaction() as db:
            try:
                await db.delete(user)
                await db.commit()
                
                app_logger.log_success(
                    "User account deleted successfully",
                    extra=context
                )
            
            except SQLAlchemyError as e:
                app_logger.log_error(
                    "Database error occurred while deleting user account",
                    error=str(e),
                    extra=context
                )
                raise DatabaseError("Error deleting user account")
            
            except Exception as e:
                app_logger.log_error(
                    "Unexpected error occurred while deleting user account",
                    error=str(e),
                    extra=context
                )
                raise DatabaseError("Error deleting user account")


    async def _send_activation_email(
        self, 
        user: User, 
        token: str, 
        custom_url: Optional[str] = None
    ) -> None:
        """
        Send activation email using the EmailService
        """
        try:
            template_data = {
                "username": user.username
            }
            
            result = await self._email_service.send_template_email(
                template=EmailTemplate.ACCOUNT_ACTIVATION,
                to_email=user.email,
                template_data=template_data,
                token=token,
                custom_url=custom_url
            )
            
            if not result.success:
                error_msg = f"Failed to send activation email: {result.error}"
                app_logger.log_error(
                    error_msg,
                    extra={
                        "user_id": str(user.id),
                        "email": user.email,
                        "template": EmailTemplate.ACCOUNT_ACTIVATION.value,
                        "metadata": result.metadata.dict() if result.metadata else None
                    }
                )
                raise EmailSendError(error_msg)

            app_logger.log_success(
                "Successfully sent activation email",
                extra={
                    "user_id": str(user.id),
                    "email": user.email,
                    "template": EmailTemplate.ACCOUNT_ACTIVATION.value,
                    "message_id": result.message_id,
                    "metadata": result.metadata.dict() if result.metadata else None
                }
            )

        except Exception as e:
            error_msg = f"Error sending activation email: {str(e)}"
            app_logger.log_error(
                error_msg,
                extra={
                    "user_id": str(user.id) if user else None,
                    "email": user.email if user else None,
                    "template": EmailTemplate.ACCOUNT_ACTIVATION.value,
                    "error": str(e)
                }
            )
            raise EmailSendError(error_msg)

    async def _update_fields(self, user: User, update_data: dict) -> None:
        """Update user fields with validation"""
        for field, value in update_data.items():
            if not hasattr(user, field):
                raise InvalidFieldException(f"Invalid field: {field}")
            setattr(user, field, value)
        await self.db.flush()

    async def _handle_integrity_error(self, error: IntegrityError) -> None:
        """Handle database integrity errors"""
        error_msg = str(error.orig).lower()
        if "email" in error_msg:
            raise InvalidDataException("This email is already registered.")
        elif "username" in error_msg:
            raise InvalidDataException("This username is already taken.")
        else:
            raise InvalidDataException("Data validation failed: duplicate entry detected.")

    def _log_database_error(self, message: str, error: Exception, context: dict) -> None:
        """Log database errors"""
        app_logger.log_error(message, error=error, extra=context)

    def _log_email_error(self, error: Exception, user: Optional[User], context: dict) -> None:
        """Log email-related errors"""
        app_logger.log_error(
            "Failed to send activation email",
            error=error,
            extra={**context, "user_id": str(user.id) if user else None}
        )
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by their email address.
        
        Args:
            email: The email address to search for
            
        Returns:
            Optional[User]: The user if found, None otherwise
        """
        context = self._log_context("get_by_email", email=email)
        
        try:
            query = select(self.model).filter(self.model.email == email)
            result = await self.db.execute(query)
            user = result.scalar_one_or_none()
            
            if user:
                app_logger.log_success(
                    "Retrieved user by email",
                    extra=context
                )
            
            return user
            
        except Exception as e:
            app_logger.log_error(
                f"Error retrieving user by email: {str(e)}",
                error=e,
                extra=context
            )
            raise DatabaseError(f"Error retrieving user by email: {str(e)}")
    

    @log_operation("get_inactive_user_by_email")
    async def get_inactive_user_by_email(self, email: str) -> User:
        """
        Retrieve an inactive user by email.

        Args:
            email: The email of the inactive user to retrieve.

        Returns:
            User: The inactive user object.

        Raises:
            NotFoundException: If the user does not exist or is already active.
            DatabaseError: If there's a database error.
        """
        try:
            result = await self.db.execute(
                select(User).where(User.email == email, not User.is_active)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                app_logger.log_error(
                    "Inactive user not found",
                    extra={"email": email}
                )
                raise NotFoundException("User", email)
            
            app_logger.log_success(
                "Inactive user retrieved successfully",
                extra={"user_id": str(user.id), "email": user.email}
            )
            return user

        except SQLAlchemyError as e:
            app_logger.log_error(
                "Database error occurred while retrieving inactive user",
                error=str(e),
                extra={"email": email}
            )
            raise DatabaseError("Error retrieving inactive user")