from datetime import datetime, timedelta
import os
import pytz
import secrets
import uuid
from typing import Optional, List

from email_validator import validate_email, EmailNotValidError
from slugify import slugify
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    event,
    inspect,
    select
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import validates, relationship, object_session
from sqlalchemy.sql import func

from app.core.logging import app_logger, log_operation
from app.database.base_model import BaseModel
from app.exceptions.database import (
    InvalidDataException,
    DatabaseCommitException,
    NotFoundException,
    TokenExpiredError
)
from app.models.tokens import Token
from app.models.roles import Role
from app.models.models import user_roles
from app.utils.password import PasswordHasher

# Environment variables with defaults
ACCOUNT_UNLOCK_DURATION = int(os.getenv("ACCOUNT_UNLOCK_DURATION", 15))
DEFAULT_ROLE_NAME = os.getenv("DEFAULT_ROLE_NAME", "user")
ACCOUNT_ACTIVATION_EXPIRES = int(os.getenv("ACCOUNT_ACTIVATION_EXPIRES", 24))

class User(BaseModel):
    """
    User model representing application users with authentication and authorization capabilities.
    """
    __tablename__ = 'users'
    
    # Primary columns
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    slug = Column(String, unique=True, nullable=False, index=True)
    
    # Status flags
    is_active = Column(Boolean, server_default='false')
    is_locked = Column(Boolean, default=False)
    
    # Authentication tracking
    login_attempts = Column(Integer, default=0)
    last_login_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    last_login_ip = Column(String(255), nullable=True, index=True)
    account_unlock = Column(DateTime, nullable=True)

    # Relationships
    tokens = relationship("Token", back_populates="user", cascade="all, delete-orphan")
    roles = relationship(
        "Role",
        secondary=user_roles,
        back_populates="users",
        lazy='selectin'
    )

    @validates('username')
    def validate_username(self, key: str, username: str) -> str:
        """Validate username length and format."""
        try:
            if not username:
                raise ValueError("Username cannot be empty")
            if len(username) < 3 or len(username) > 32:
                raise ValueError("Username should be between 3 and 32 characters long")
            return username
        except ValueError as e:
            app_logger.log_error(
                "Username validation failed",
                error=e,
                extra={"username": username}
            )
            raise

    @validates('email')
    def validate_email(self, key: str, email_address: str) -> str:
        """Validate email format."""
        try:
            valid = validate_email(email_address)
            return valid.email
        except EmailNotValidError as e:
            app_logger.log_error(
                "Email validation failed",
                error=e,
                extra={"email": email_address}
            )
            raise ValueError(str(e))

    def generate_slug(self) -> str:
        """Generate a unique slug from the username."""
        try:
            base_slug = slugify(self.username)
            slug = base_slug
            counter = 1

            while True:
                existing_slug = (
                    object_session(self)
                    .query(User)
                    .filter(User.slug == slug, User.id != self.id)
                    .first()
                )
                if not existing_slug:
                    break
                slug = f"{base_slug}-{counter}"
                counter += 1
            return slug
        except Exception as e:
            app_logger.log_error(
                "Slug generation failed",
                error=e,
                extra={"username": self.username}
            )
            raise

    @log_operation("create_activation_token")
    async def create_activation_token(self, session: AsyncSession) -> Token:
        """Create and save a new activation token."""
        if not self.id:
            raise ValueError("User ID is not set. Cannot create activation token.")
        
        try:
            token_string = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(hours=ACCOUNT_ACTIVATION_EXPIRES)
            
            token = Token(
                user_id=self.id,
                token=token_string,
                token_type='activation',
                expires_at=expires_at
            )
            
            session.add(token)
            await session.flush()
            return token
        except Exception as e:
            app_logger.log_error(
                "Failed to create activation token",
                error=e,
                extra={"user_id": str(self.id)}
            )
            raise

    @log_operation("create_password_reset_token")
    async def create_password_reset_token(self, session: AsyncSession) -> Token:
        """Create and save a password reset token."""
        try:
            token_string = str(uuid.uuid4())
            expires_at = datetime.now() + timedelta(hours=24)
            
            token = Token(
                user_id=self.id,
                token=token_string,
                token_type='password_reset',
                expires_at=expires_at
            )
            
            session.add(token)
            return token
        except Exception as e:
            app_logger.log_error(
                "Failed to create password reset token",
                error=e,
                extra={"user_id": str(self.id)}
            )
            raise

    async def verify_token(self, token: str, token_type: str) -> bool:
        """Verify if a given token is valid and not expired."""
        try:
            token_record = next(
                (t for t in self.tokens if t.token == token and t.token_type == token_type),
                None
            )
            
            if not token_record:
                return False
                
            if token_record.expires_at < datetime.now(pytz.utc):
                raise TokenExpiredError("Token has expired")
                
            return True
        except TokenExpiredError:
            raise
        except Exception as e:
            app_logger.log_error(
                "Token verification failed",
                error=e,
                extra={"user_id": str(self.id)}
            )
            raise

    def check_password(self, password: str) -> bool:
        """Verify if the provided password matches the stored hash."""
        try:
            return PasswordHasher.verify_password(password, self.password_hash)
        except Exception as e:
            app_logger.log_error(
                "Password check failed",
                error=e,
                extra={"user_id": str(self.id)}
            )
            raise

    def set_password(self, password: str) -> None:
        """Hash and set the user's password."""
        try:
            self.password_hash = PasswordHasher.get_password_hash(password)
        except Exception as e:
            app_logger.log_error(
                "Setting password failed",
                error=e,
                extra={"user_id": str(self.id)}
            )
            raise

    def reset_login_attempts(self) -> None:
        """Reset failed login attempts and unlock account."""
        try:
            self.login_attempts = 0
            self.is_locked = False
            self.account_unlock = None
        except Exception as e:
            app_logger.log_error(
                "Resetting login attempts failed",
                error=e,
                extra={"user_id": str(self.id)}
            )
            raise

    def increment_login_attempts(self, max_attempts: int) -> None:
        """Increment failed login attempts and lock account if threshold reached."""
        try:
            self.login_attempts += 1
            if self.login_attempts >= max_attempts:
                self.is_locked = True
                self.account_unlock = datetime.now() + timedelta(minutes=ACCOUNT_UNLOCK_DURATION)
        except Exception as e:
            app_logger.log_error(
                "Incrementing login attempts failed",
                error=e,
                extra={"user_id": str(self.id)}
            )
            raise

    def add_role(self, role: Role) -> None:
        """Add a role to the user if not already assigned."""
        if role not in self.roles:
            self.roles.append(role)
            
    def remove_role(self, role: Role) -> None:
        """Remove a role from the user if assigned."""
        if role in self.roles:
            self.roles.remove(role)

    @property
    def is_anonymous(self) -> bool:
        """Check if the user is anonymous."""
        return False
    
    @property
    def is_admin(self) -> bool:
        """Check if the user has admin role."""
        try:
            return any(role.name.lower() == "admin" for role in self.roles)
        except Exception as e:
            app_logger.log_error(
                "Admin check failed",
                error=e,
                extra={"user_id": str(self.id)}
            )
            return False
    
    def has_role(self, role_name: str) -> bool:
        """Check if user has a specific role."""
        try:
            return any(role.name.lower() == role_name.lower() for role in self.roles)
        except Exception as e:
            app_logger.log_error(
                "Role check failed",
                error=e,
                extra={"user_id": str(self.id), "role_name": role_name}
            )
            return False

    @property
    def assigned_roles(self) -> List[Role]:
        """Get list of assigned roles."""
        return self.roles

    @property
    def account_locked_until(self) -> Optional[datetime]:
        """Get datetime when account will be unlocked."""
        return self.account_unlock if self.is_locked else None

# SQLAlchemy Event Listeners
@event.listens_for(User, 'before_insert')
def generate_slug_on_insert(mapper, connection, target):
    """Generate slug before inserting new user."""
    if target.username:
        try:
            target.slug = target.generate_slug()
        except Exception as e:
            app_logger.log_error(
                "Generating slug on insert failed",
                error=e,
                extra={"username": target.username}
            )
            raise

@event.listens_for(User, 'before_update')
def generate_slug_on_update(mapper, connection, target):
    """Update slug if username changes."""
    if inspect(target).attrs.username.history.has_changes() and target.username:
        try:
            target.slug = target.generate_slug()
        except Exception as e:
            app_logger.log_error(
                "Updating slug failed",
                error=e,
                extra={"username": target.username}
            )
            raise

@event.listens_for(User, 'after_insert')
def assign_default_role(mapper, connection, target):
    """Assign default role to newly created user."""
    try:
        role_id_query = select(Role.id).filter(Role.name == DEFAULT_ROLE_NAME)
        role_id = connection.scalar(role_id_query)
        
        if role_id:
            connection.execute(
                user_roles.insert().values(
                    user_id=target.id,
                    role_id=role_id
                )
            )
    except SQLAlchemyError as e:
        app_logger.log_error(
            "Failed to assign default role",
            error=e,
            extra={"user_id": str(target.id)}
        )
        raise InvalidDataException(f"Failed to assign default role: {str(e)}")