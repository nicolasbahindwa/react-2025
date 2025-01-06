from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    api_title: str = "AGENT BRAIN"
    api_description: str = "A multi-agent application"
    api_version: str = "0.1.0"
    allow_origins: str = "*"
    is_development: bool = True 
    
    # Database settings
    db_name: str = ""
    db_user: str = ""
    db_password: str = ""
    
    # Development settings
    reload_delay: float = 0.25
    reload_dirs: List[str] = ["app"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@localhost:5432/{self.db_name}"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()