from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class EmailSettings(BaseSettings):
    """Email configuration settings using pydantic"""
    SMTP_HOST: str = "sandbox.smtp.mailtrap.io"
    SMTP_PORT: int = 2525
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_USE_TLS: bool = False
    
    MAIL_FROM: str = "mail"
    MAIL_FROM_NAME: str = "FastAPI App"
    FRONT_END_URL: str = "http://localhost:3000"
    LOGIN_URL: str = "http://localhost:3000/login"
    
    EMAIL_DEBUG_MODE: bool = False
    
    class Config:
        env_file = ".env"
        # case_sensitive = True
        # env_file_encoding = "utf-8"
        extra = 'allow'

@lru_cache(maxsize=None)
def get_email_settings() -> EmailSettings:
    """Get cached email settings"""
    return EmailSettings()