"""
Configuration management for Lake Holidays Challenge API
Handles environment variables and application settings
"""

from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = "Lake Holidays Challenge API"
    version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    algorithm: str = "HS256"
    
    # Database
    database_url: str = "postgresql+asyncpg://postgres:password@localhost:5432/lake_holidays"
    
    # Redis (for caching and sessions)
    redis_url: str = "redis://localhost:6379/0"
    
    # OAuth Configuration
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    microsoft_client_id: Optional[str] = None
    microsoft_client_secret: Optional[str] = None
    
    # AI Services
    openai_api_key: Optional[str] = None
    azure_openai_endpoint: Optional[str] = None
    azure_openai_api_key: Optional[str] = None
    azure_openai_api_version: str = "2023-12-01-preview"
    
    # Azure Storage
    azure_storage_connection_string: Optional[str] = None
    azure_storage_container_name: str = "lake-holidays-media"
    
    # File Upload
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_image_types: list[str] = ["image/jpeg", "image/png", "image/webp"]
    
    # CORS
    cors_origins: list[str] = [
        "http://localhost:3000",  # React dev server
        "http://localhost:5173",  # Vite dev server
        "https://lake-holidays-app.azurewebsites.net"  # Production frontend
    ]
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    
    # Geography
    default_timezone: str = "UTC"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()


# Global settings instance
settings = get_settings()
