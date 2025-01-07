import os
from dotenv import load_dotenv
from pydantic_settings  import BaseSettings
from pydantic import Field
from datetime import timedelta

load_dotenv()  # Load environment variables from .env file

class Settings(BaseSettings):
    api_title: str = "FastAPI"
    api_description: str = "FastAPI Application"
    api_version: str = "1.0.0"
    allow_origins: str = "*"
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    database_url: str
    secret_key: str
    debug: bool
    jwt_secret_key: str
    jwt_refresh_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    minimum_password_length: int = 8
    password_reset_token_expire_minutes: int = 15

    class Config:
        env_file = ".env"
        extra = "allow"

# Instantiate settings
settings = Settings()

# Example usage
print(settings.api_title)
print(settings.jwt_secret_key)
