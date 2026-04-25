"""Application configuration settings."""
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # Database
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://cinema_user:cinema_password@localhost:5432/cinema_db"
    )
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
    
    # Debug mode
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Allowed hosts
    allowed_hosts: list[str] = ["localhost", "127.0.0.1", "0.0.0.0"]
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = False


settings = Settings()
