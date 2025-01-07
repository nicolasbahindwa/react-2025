# from fastapi import APIRouter, Depends, status, BackgroundTasks, HTTPException
# from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
# from sqlalchemy.ext.asyncio import AsyncSession
# from pydantic import EmailStr, BaseModel
# from app.database import get_db

# from app.services.token_service import TokenService
# from app.services.email import EmailService
# from app.services.auth_service import AuthService
# from app.models.users import User
# from app.exceptions.database import (
#     DatabaseError, InvalidTokenError, TokenExpiredError, DatabaseCommitException
# )
# from app.schemas.user import UserResponse
# from app.schemas.auth import TokenSchema, UserLogin, ResetPassword
# from app.schemas.token import RefreshTokenRequest
# from app.repositories.auth import AuthRepository, get_auth_repository

# router = APIRouter(prefix="/auth", tags=["authentication"])

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/token", scheme_name="OAuth2PasswordBearer")

# async def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
#     return AuthService(db)

# async def get_email_service() -> EmailService:
#     return EmailService()

# class TestEmailSchema(BaseModel):
#     to_email: EmailStr
#     subject: str = "Test Email"
#     username: str = "Test User"

# @router.post("/test-email")
# async def test_email(
#     email_data: TestEmailSchema,
#     background_tasks: BackgroundTasks,
#     email_service: EmailService = Depends(get_email_service)
# ):
#     """Test endpoint to send a test email"""
#     try:
#         background_tasks.add_task(
#             email_service.send_email,
#             to_email=email_data.to_email,
#             subject=email_data.subject,
#             template_name="test_email",
#             template_data={"username": email_data.username}
#         )
#         return {"message": f"Test email queued for sending to {email_data.to_email}"}
#     except Exception as e:
#         raise DatabaseError(detail=f"Failed to send test email: {str(e)}")

 
# @router.post("/activate/{token}", response_model=UserResponse)
# async def activate_account(
#     token: str, 
#     background_tasks: BackgroundTasks,
#     db: AsyncSession = Depends(get_db),
#     email_service: EmailService = Depends(get_email_service)
# ):
#     auth_service = AuthService(db)
#     try:
#         user = await auth_service.process_account_activation(token)
        
#         return user
#     except InvalidTokenError:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Invalid activation token"
#         )
#     except TokenExpiredError:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Activation token has expired"
#         )
#     except DatabaseCommitException as e:
#         raise DatabaseError(detail=str(e))

# @router.post('/resend-activation', response_model=dict)
# async def resend_activation(
#     email: str,
#     auth_service: AuthService = Depends(get_auth_service)
# ):
#     """Endpoint to resend activation email"""
#     try:
#         user, _ = await auth_service.resend_activation_token(email)
#         return {"message": "New activation token sent to your email"}
#     except DatabaseCommitException as e:
#         raise DatabaseError(detail=str(e))

# @router.post("/request-password-reset")
# async def request_password_reset(
#     email: EmailStr,
#     auth_service: AuthService = Depends(get_auth_service)
# ):
#     """Endpoint to request password reset"""
#     try:
#         result = await auth_service.request_password_reset(email)
#         return {
#             "message": "Password reset instructions sent to your email",
#             "token": result.get("token") # Only returned in debug mode
#         }
#     except Exception as e:
#         raise DatabaseError(detail=f"Failed to process password reset request: {str(e)}")



# @router.post("/reset-password")
# async def reset_password(reset_data: ResetPassword, auth_service: AuthService = Depends(get_auth_service)):
#     try:
#         return await auth_service.reset_password(token=reset_data.token, new_password=reset_data.new_password)
#     except InvalidTokenError as e:
#         raise e
#     except DatabaseCommitException as e:
#         raise DatabaseError(detail=str(e))

# @router.post("/login/token", response_model=TokenSchema)
# async def login_for_swagger(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends(get_auth_service)):
#     return await auth_service.authenticate_user(email=form_data.username, password=form_data.password)

# @router.post("/login", response_model=TokenSchema)
# async def login_for_api(login_data: UserLogin, auth_service: AuthService = Depends(get_auth_service)):
#     return await auth_service.authenticate_user(email=login_data.email, password=login_data.password)

# @router.post("/refresh-token", response_model=TokenSchema)
# async def refresh_token(refresh_data: RefreshTokenRequest, auth_service: AuthService = Depends(get_auth_service)):
#     try:
#         return await auth_service.refresh_access_token(refresh_data.refresh_token)
#     except InvalidTokenError as e:
#         raise e
#     except TokenExpiredError as e:
#         raise e

# @router.post("/logout")
# async def logout(
#     auth_repo: AuthRepository = Depends(get_auth_repository),
#     token: str = Depends(AuthRepository.oauth2_scheme)
# ):
#     user = await auth_repo.get_current_user(token)
#     db = auth_repo.session
#     token_service = TokenService(db)
#     await token_service.revoke_all_user_tokens(user.id)
#     return {"message": "Successfully logged out"}


# @router.get("/me", response_model=UserResponse)
# async def get_me(
#     auth_repo: AuthRepository = Depends(get_auth_repository),
#     token: str = Depends(oauth2_scheme)  # Use the global `oauth2_scheme`
# ):
#     return await auth_repo.get_current_user(token)

# @router.post("/admin/logout/all-users")
# async def logout_all_users(
#     auth_repo: AuthRepository = Depends(get_auth_repository),
#     token: str = Depends(oauth2_scheme)  # Use the global `oauth2_scheme`
# ):
#     admin_user = await auth_repo.get_admin_user(token)
#     db = auth_repo.session
#     token_service = TokenService(db)
#     # Revoke tokens for all users
#     return {"message": "Successfully logged out all users"}




from fastapi import APIRouter, Depends, status, BackgroundTasks, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from pydantic import EmailStr, BaseModel

from app.database import get_db
from app.services.token_service import TokenService
from app.services.email import EmailService
from app.services.auth_service import AuthService
from app.models.users import User
from app.repositories.auth import AuthRepository, get_auth_repository
from app.exceptions.database import (
    DatabaseError, InvalidTokenError, TokenExpiredError, DatabaseCommitException,InvalidDataException
)
from app.schemas.user import UserResponse
from app.schemas.auth import TokenSchema, UserLogin, ResetPassword
from app.schemas.token import RefreshTokenRequest

router = APIRouter(prefix="/auth", tags=["authentication"])

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login/token",  # Remove the leading slash
    scheme_name="OAuth2PasswordBearer"
)
# Dependency functions
async def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)

async def get_email_service() -> EmailService:
    return EmailService()

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_repo: AuthRepository = Depends(get_auth_repository)
) -> User:
    """
    Dependency to get the current authenticated user from a token.
    """
    user = await auth_repo.get_user_by_token(token)
    return await auth_repo.verify_active_user(user)

async def get_admin_user(
    current_user: User = Depends(get_current_user),
    auth_repo: AuthRepository = Depends(get_auth_repository)
) -> User:
    """
    Dependency to get current user and verify they have admin privileges.
    """
    return await auth_repo.verify_admin_user(current_user)

# Type aliases for cleaner dependency injection
CurrentUser = Annotated[User, Depends(get_current_user)]
AdminUser = Annotated[User, Depends(get_admin_user)]

# Test email endpoint schema
class TestEmailSchema(BaseModel):
    to_email: EmailStr
    subject: str = "Test Email"
    username: str = "Test User"

@router.post("/test-email")
async def test_email(
    email_data: TestEmailSchema,
    background_tasks: BackgroundTasks,
    email_service: EmailService = Depends(get_email_service)
):
    """Test endpoint to send a test email"""
    try:
        background_tasks.add_task(
            email_service.send_email,
            to_email=email_data.to_email,
            subject=email_data.subject,
            template_name="test_email",
            template_data={"username": email_data.username}
        )
        return {"message": f"Test email queued for sending to {email_data.to_email}"}
    except Exception as e:
        raise DatabaseError(detail=f"Failed to send test email: {str(e)}")

@router.post("/activate/{token}", response_model=UserResponse)
async def activate_account(
    token: str, 
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    email_service: EmailService = Depends(get_email_service)
):
    auth_service = AuthService(db)
    try:
        user = await auth_service.process_account_activation(token)
      
        return user
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid activation token"
        )
    except TokenExpiredError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Activation token has expired"
        )
    except DatabaseCommitException as e:
        raise DatabaseError(detail=str(e))

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: CurrentUser):
    """Get current user's information"""
    return current_user

@router.get("/users", response_model=list[UserResponse])
async def get_users(
    admin_user: AdminUser,
    auth_repo: AuthRepository = Depends(get_auth_repository)
):
    """Get all users (admin only)"""
    return await auth_repo.get_all_users()

@router.post('/resend-activation', response_model=dict)
async def resend_activation(
    email: str,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Endpoint to resend activation email"""
    try:
        user, _ = await auth_service.resend_activation_token(email)
        return {"message": "New activation token sent to your email"}
    except DatabaseCommitException as e:
        raise DatabaseError(detail=str(e))

@router.post("/request-password-reset")
async def request_password_reset(
    email: EmailStr,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Endpoint to request password reset"""
    try:
        result = await auth_service.request_password_reset(email)
        return {
            "message": "Password reset instructions sent to your email",
            "token": result.get("token") # Only returned in debug mode
        }
    except Exception as e:
        raise DatabaseError(detail=f"Failed to process password reset request: {str(e)}")

@router.post("/reset-password")
async def reset_password(
    reset_data: ResetPassword, 
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        return await auth_service.reset_password(
            token=reset_data.token, 
            new_password=reset_data.new_password
        )
    except InvalidTokenError as e:
        raise e
    except DatabaseCommitException as e:
        raise DatabaseError(detail=str(e))

@router.post("/login/token", response_model=TokenSchema)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    Used by Swagger UI.
    """
    print("***************************")
    print(form_data.username)
    try:
        tokens = await auth_service.authenticate_user(
            email=form_data.username,  # OAuth2 uses username field for email
            password=form_data.password
        )
        return tokens
    except InvalidDataException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/login", response_model=TokenSchema)
async def login_for_api(
    login_data: UserLogin, 
    auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.authenticate_user(
        email=login_data.email, 
        password=login_data.password
    )

@router.post("/refresh-token", response_model=TokenSchema)
async def refresh_token(
    refresh_data: RefreshTokenRequest, 
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        return await auth_service.refresh_access_token(refresh_data.refresh_token)
    except (InvalidTokenError, TokenExpiredError) as e:
        raise e

@router.post("/logout")
async def logout(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    try:
        token_service = TokenService(db)
        await token_service.revoke_all_user_tokens(current_user.id)
        return {"message": "Successfully logged out"}
    except DatabaseCommitException as e:
        raise DatabaseError(detail=str(e))

@router.post("/admin/logout/all-users")
async def logout_all_users(
    admin_user: AdminUser,
    auth_repo: AuthRepository = Depends(get_auth_repository)
):
    """Revoke tokens for all users (admin only)"""
    try:
        users = await auth_repo.get_all_users()
        token_service = TokenService(auth_repo._session)
        for user in users:
            await token_service.revoke_all_user_tokens(user.id)
        return {"message": "Successfully logged out all users"}
    except DatabaseCommitException as e:
        raise DatabaseError(detail=str(e))

@router.post("/admin/revoke/{user_id}")
async def revoke_user_access(
    user_id: str,
    admin_user: AdminUser,
    auth_repo: AuthRepository = Depends(get_auth_repository)
):
    """Revoke a specific user's access (admin only)"""
    try:
        user = await auth_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        user.is_active = False
        await auth_repo.update(user)
        return {"message": f"Access revoked for user {user_id}"}
    except DatabaseCommitException as e:
        raise DatabaseError(detail=str(e))