from typing import Optional, Tuple
from datetime import datetime, timezone
from fastapi import Depends
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, or_
from sqlalchemy.exc import SQLAlchemyError

from app.database.session import get_db_session, managed_transaction
from app.services.email import EmailService
from app.models.email import EmailTemplate
from app.schemas.auth import TokenSchema
from app.schemas.user import UserResponse
from app.models.users import User
from app.models.tokens import Token, ALLOWED_TOKEN_TYPES
from app.core.logging import app_logger, log_operation
from app.utils.emailSettings import get_email_settings
from app.services.token_service import TokenService
from app.repositories.user import UserRepository
from app.exceptions.database import (
    DatabaseError, NotFoundException, InvalidDataException,
    DatabaseCommitException, TokenExpiredError, InvalidTokenError,
    EmailSendError, TokenCreationError,
    
)
from app.repositories.base import BaseRepository
from pydantic import EmailStr
 
import os
ACCOUNT_UNLOCK_DURATION = int(os.getenv("ACCOUNT_UNLOCK_DURATION", 15))
MAX_LOGIN_ATTEMPTS = int(os.getenv("MAX_LOGIN_ATTEMPTS", 5))
class AuthService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_db_session),
        email_service: Optional[EmailService] = None,
        token_service: Optional[TokenService] = None,
        user_repository: Optional[UserRepository] = None,
        
    ):
        self._session = session
        self._settings = get_email_settings()
        self._email_service = email_service or EmailService()
        self._token_service = token_service or TokenService(session)
        self._user_repo = user_repository or UserRepository(session)
    
    
    @log_operation("authenticate_user")
    async def authenticate_user(self, email: str, password: str) -> TokenSchema:
        try:
            user = await self._user_repo.get_by_email(email)
            if not user:
                raise InvalidDataException("Invalid email or password")

            if user.is_locked and user.account_unlock and user.account_unlock > datetime.now():
                raise InvalidDataException(f"Account is locked. Please try again after {user.account_unlock}")

            if not user.check_password(password):
                async with managed_transaction():
                    await self._handle_failed_login(user)
                raise InvalidDataException("Invalid email or password")

            if not user.is_active:
                raise InvalidDataException("Account is not activated. Please check your email for activation instructions")

            async with managed_transaction():
                await self._handle_successful_login(user)
                tokens = await self._token_service.create_token_pair(user.id)
                
                return TokenSchema(
                    access_token=tokens[0],
                    token_type="bearer",
                    refresh_token=tokens[1]
                )

        except SQLAlchemyError as e:
            app_logger.log_error(
                "Database error during authentication",
                error=str(e),
                extra={"email": email}
            )
            raise DatabaseError(f"Authentication failed: {str(e)}")
        except Exception as e:
            app_logger.log_error(
                "Authentication failed",
                error=str(e),
                extra={"email": email}
            )
            raise



    @log_operation("process_account_activation")
    async def process_account_activation(
        self, 
        token_string: str, 
        custom_url: Optional[str] = None
    ) -> UserResponse:
        try:
            token_user = await self._token_service.get_active_token_with_user(
                token_string=token_string,
                token_type=ALLOWED_TOKEN_TYPES['activation']
            )
        
            if not token_user:
                raise InvalidTokenError(
                    "Invalid activation token",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            token, user = token_user
        
            await self._validate_activation_token(token)
            
            if user.is_active:
                async with managed_transaction():
                    await self._handle_already_active_user(token)
                return user
        
            async with managed_transaction():
                user.is_active = True
                user.email_verified_at = datetime.now(timezone.utc)
                await self._token_service.revoke_all_user_tokens(user.id)
                await self._session.refresh(user)

                try:
                    await self._send_activation_confirmation_email(user, custom_url)
                except EmailSendError as e:
                    app_logger.log_error(
                        "Failed to send activation confirmation email",
                        error=str(e),
                        extra={"user_id": str(user.id), "email": user.email}
                    )
                    # Continue activation even if email fails

                return user

        except (InvalidTokenError, TokenExpiredError) as e:
            raise
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error during activation: {str(e)}")
        except Exception as e:
            app_logger.log_error(
                "Account activation failed",
                error=str(e),
                extra={"token": token_string}
            )
            raise DatabaseError("Failed to activate account")


    @log_operation("request_password_reset")
    async def request_password_reset(
        self, 
        email: str, 
        custom_url: Optional[str] = None
    ) -> dict:
        try:
            user = await self._user_repo.get_by_email(email)
            if not user:
                raise NotFoundException("User", email)

            async with managed_transaction():
                token = await self._create_and_send_reset_token(user, custom_url)
                
                response = {"message": "Password reset email sent successfully"}
                if self._settings.EMAIL_DEBUG_MODE:
                    response["token"] = token.token
                return response

        except (NotFoundException, EmailSendError) as e:
            raise
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database error during password reset request: {str(e)}")
        except Exception as e:
            app_logger.log_error(
                "Password reset request failed",
                error=str(e),
                extra={"email": email}
            )
            raise DatabaseError("Failed to process password reset request")
    
    @log_operation("resend_activation_token")
    async def resend_activation_token(self, email: str, custom_url: Optional[str] = None) -> Tuple[User, str]:
        try:
            user = await self._user_repo.get_inactive_user_by_email(email)
            if not user:
                raise NotFoundException("User not found or already activated")

            async with managed_transaction():
                # Create activation token
                token = await user.create_activation_token(session=self._session)
                
                try:
                
                    await self._send_email_with_logging(
                        template=EmailTemplate.ACCOUNT_ACTIVATION,
                        to_email=user.email,
                        template_data={"username": user.username},
                        operation_name="account activation",
                        token=token.token,
                        custom_url=custom_url
                    )
                    
                except EmailSendError:
                    # Revoke the token if email sending fails
                    await self._token_service.revoke_token(token)
                    raise

            return user, token.token

        except Exception as e:
            app_logger.log_error("Error during resend activation token", error=str(e))
            raise DatabaseError("Error generating new activation token")


    @log_operation("reset_password")
    async def reset_password(self, token: str, new_password: str) -> dict:
        try:
            token_obj = await self._token_service.get_valid_reset_token(token)
            if not token_obj:
                raise InvalidTokenError(
                    "Invalid or expired reset token",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            user = await self._user_repo.get_by_id(token_obj.user_id)
            if not user:
                raise NotFoundException("User", token_obj.user_id)

            async with managed_transaction():
                user.set_password(new_password)
                await self._token_service.revoke_all_user_tokens(user.id)
                
                app_logger.log_success(
                    "Password reset successful",
                    extra={"user_id": str(user.id)}
                )

                return {"message": "Password successfully reset"}

        except (InvalidTokenError, NotFoundException) as e:
            raise
        except SQLAlchemyError as e:
            raise DatabaseCommitException(f"Failed to reset password: {str(e)}")
        except Exception as e:
            app_logger.log_error(
                "Password reset failed",
                error=str(e),
                extra={"token": token}
            )
            raise DatabaseError("Failed to process password reset")

    # Helper methods
    async def _send_activation_confirmation_email(
        self,
        user: User,
        custom_url: Optional[str] = None
    ) -> None:
        """Send activation confirmation email using updated EmailService"""
        await self._send_email_with_logging(
            template=EmailTemplate.ACCOUNT_ACTIVATION_CONFIRM,
            to_email=user.email,
            template_data={"username": user.username},
            operation_name="account activation confirmation",
            custom_url=custom_url
        )

    async def _handle_failed_login(self, user: User) -> None:
        user.increment_login_attempts(MAX_LOGIN_ATTEMPTS)
        await self._session.flush()

    async def _handle_successful_login(self, user: User) -> None:
        user.reset_login_attempts()
        user.last_login_at = datetime.now(timezone.utc)
        await self._session.flush()

    async def _handle_already_active_user(self, token: Token) -> None:
        await self._token_service.revoke_token(token)
        
    async def _validate_activation_token(self, token: Token) -> None:
        if token.is_expired():
            async with managed_transaction():
                await self._token_service.revoke_token(token)
            raise TokenExpiredError()
    
    async def _send_email_with_logging(
        self,
        template: EmailTemplate,
        to_email: EmailStr,
        template_data: dict,
        operation_name: str,
        token: Optional[str] = None,
        custom_url: Optional[str] = None
    ) -> None:
        """
        Send an email with comprehensive logging and error handling using EmailService
        """
        try:
            result = await self._email_service.send_template_email(
                template=template,
                to_email=to_email,
                template_data=template_data,
                token=token,
                custom_url=custom_url
            )
            
            if not result.success:
                error_msg = f"Failed to send {operation_name} email: {result.error}"
                app_logger.log_error(
                    error_msg,
                    extra={
                        "email": to_email,
                        "template": template.value,
                        "operation": operation_name,
                        "metadata": result.metadata.dict() if result.metadata else None
                    }
                )
                raise EmailSendError(error_msg)

            app_logger.log_success(
                f"Successfully sent {operation_name} email",
                extra={
                    "email": to_email,
                    "template": template.value,
                    "operation": operation_name,
                    "message_id": result.message_id,
                    "metadata": result.metadata.dict() if result.metadata else None
                }
            )
                
        except Exception as e:
            error_msg = f"Error sending {operation_name} email: {str(e)}"
            app_logger.log_error(
                error_msg,
                extra={
                    "email": to_email,
                    "template": template.value,
                    "operation": operation_name,
                    "error": str(e)
                }
            )
            raise EmailSendError(error_msg)

    async def _send_activation_confirmation_email(
        self,
        user: User,
        custom_url: Optional[str] = None
    ) -> None:
        """Send activation confirmation email using EmailService"""
        template_data = {
            "username": user.username
        }
        
        await self._send_email_with_logging(
            template=EmailTemplate.ACCOUNT_ACTIVATION_CONFIRM,
            to_email=user.email,
            template_data=template_data,
            operation_name="account activation confirmation",
            custom_url=custom_url
        )

    async def _create_and_send_reset_token(
        self,
        user: User,
        custom_url: Optional[str] = None
    ) -> Token:
        """Create and send password reset token using EmailService"""
        token = await user.create_password_reset_token(session=self._session)
        
        try:
            template_data = {
                "username": user.username
            }
            
            await self._send_email_with_logging(
                template=EmailTemplate.PASSWORD_RESET,
                to_email=user.email,
                template_data=template_data,
                operation_name="password reset",
                token=token.token,
                custom_url=custom_url
            )
        except EmailSendError:
            await self._token_service.revoke_token(token)
            raise
            
        return token

    # @log_operation("resend_activation_token")
    # async def resend_activation_token(
    #     self,
    #     email: str,
    #     custom_url: Optional[str] = None
    # ) -> Tuple[User, str]:
    #     """Resend activation token to user"""
    #     try:
    #         user = await self._user_repo.get_inactive_user_by_email(email)
    #         if not user:
    #             raise NotFoundException("User not found or already activated")

    #         async with managed_transaction():
    #             token = await user.create_activation_token(session=self._session)
                
    #             try:
    #                 template_data = {
    #                     "username": user.username
    #                 }
                    
    #                 await self._send_email_with_logging(
    #                     template=EmailTemplate.ACCOUNT_ACTIVATION,
    #                     to_email=user.email,
    #                     template_data=template_data,
    #                     operation_name="account activation",
    #                     token=token.token,
    #                     custom_url=custom_url
    #                 )
    #             except EmailSendError:
    #                 await self._token_service.revoke_token(token)
    #                 raise

    #             return user, token.token

    #     except Exception as e:
    #         app_logger.log_error("Error during resend activation token", error=str(e))
    #         raise DatabaseError("Error generating new activation token")