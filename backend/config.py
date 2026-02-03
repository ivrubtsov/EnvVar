import os
from pathlib import Path
from typing import Optional


class Config:
    """Application configuration from environment variables"""
    
    # Application
    APP_NAME: str = os.getenv('APP_NAME', 'MyApp')
    APP_VERSION: str = os.getenv('APP_VERSION', '1.0.0')
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    SECRET_KEY: str = os.environ['SECRET_KEY']
    
    # Server
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', '8000'))
    WORKERS: int = int(os.getenv('WORKERS', '4'))
    
    # Database
    DATABASE_URL: str = os.environ['DATABASE_URL']
    DB_ECHO: bool = os.getenv('DB_ECHO', 'False').lower() == 'true'
    DB_POOL_SIZE: int = int(os.getenv('DB_POOL_SIZE', '10'))
    DB_MAX_OVERFLOW: int = int(os.getenv('DB_MAX_OVERFLOW', '20'))
    
    # Redis
    REDIS_URL: str = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    REDIS_PASSWORD: Optional[str] = os.getenv('REDIS_PASSWORD')
    REDIS_TTL: int = int(os.getenv('REDIS_TTL', '3600'))
    
    # Authentication
    JWT_SECRET_KEY: str = os.environ['JWT_SECRET']
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', 'HS256')
    JWT_EXPIRATION_HOURS: int = int(os.getenv('JWT_EXPIRATION_HOURS', '24'))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS', '30'))
    
    # OAuth
    GOOGLE_CLIENT_ID: Optional[str] = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET: Optional[str] = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_REDIRECT_URI: Optional[str] = os.getenv('GOOGLE_REDIRECT_URI')
    
    GITHUB_CLIENT_ID: Optional[str] = os.getenv('GITHUB_CLIENT_ID')
    GITHUB_CLIENT_SECRET: Optional[str] = os.getenv('GITHUB_CLIENT_SECRET')
    
    # Email
    SMTP_HOST: str = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    SMTP_PORT: int = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USER: Optional[str] = os.getenv('SMTP_USER')
    SMTP_PASSWORD: Optional[str] = os.getenv('SMTP_PASSWORD')
    SMTP_TLS: bool = os.getenv('SMTP_TLS', 'True').lower() == 'true'
    
    # Storage
    UPLOAD_DIR: Path = Path(os.getenv('UPLOAD_DIR', './uploads'))
    MAX_UPLOAD_SIZE: int = int(os.getenv('MAX_UPLOAD_SIZE', '10485760'))
    ALLOWED_EXTENSIONS: list = os.getenv('ALLOWED_EXTENSIONS', 'jpg,jpeg,png,pdf').split(',')
    
    # Monitoring
    SENTRY_DSN: Optional[str] = os.getenv('SENTRY_DSN')
    SENTRY_ENVIRONMENT: str = os.getenv('SENTRY_ENVIRONMENT', 'production')
    SENTRY_TRACES_SAMPLE_RATE: float = float(os.getenv('SENTRY_TRACES_SAMPLE_RATE', '0.1'))
    
    # Feature Flags
    ENABLE_ANALYTICS: bool = os.getenv('ENABLE_ANALYTICS', 'False').lower() == 'true'
    ENABLE_BETA_FEATURES: bool = os.getenv('ENABLE_BETA_FEATURES', 'False').lower() == 'true'
    ENABLE_RATE_LIMITING: bool = os.getenv('ENABLE_RATE_LIMITING', 'True').lower() == 'true'
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv('RATE_LIMIT_PER_MINUTE', '60'))
    RATE_LIMIT_PER_HOUR: int = int(os.getenv('RATE_LIMIT_PER_HOUR', '1000'))
    
    # Celery (Background Tasks)
    CELERY_BROKER_URL: str = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/1')
    CELERY_RESULT_BACKEND: str = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/2')
    
    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT: str = os.getenv('LOG_FORMAT', 'json')
    LOG_FILE: Optional[str] = os.getenv('LOG_FILE')
    
    @classmethod
    def validate(cls):
        """Validate required environment variables"""
        required = ['SECRET_KEY', 'DATABASE_URL', 'JWT_SECRET']
        missing = [var for var in required if not os.getenv(var)]
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")


# Validate on import
Config.validate()
