from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field, validator
from functools import lru_cache
import os
from pathlib import Path
from dotenv import load_dotenv

# Determine the root directory
current_file = Path(__file__)
root_dir = current_file.parent.parent.parent.parent
env_file_path = root_dir / '.env'

# Load the .env file
load_dotenv(env_file_path)

# print(f"Loading environment variables from: {env_file_path}")
# print("Environment Variables:")
# for key, value in os.environ.items():
#     print(f"{key}: {value}")

class Settings(BaseSettings):
    API_TITLE: str = "FastAPI"
    API_DESCRIPTION: str = "FastAPI Application"
    API_VERSION: str = "1.0.0"

    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=False)

    ALLOW_ORIGINS: List[str] = Field(default=["*"])

    DATABASE_URL: str
    SECRET_KEY: str
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    MINIMUM_PASSWORD_LENGTH: int = 8
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = 20

    class Config:
        case_sensitive = True

    @validator("ALLOW_ORIGINS", pre=True)
    def parse_allow_origins(cls, v):
        if isinstance(v, str):
            return v.split(",") if v else ["*"]
        return v

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

# print("Loaded settings:")
# print(settings.dict())
