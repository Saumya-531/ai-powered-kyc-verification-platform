"""Application configuration using Pydantic BaseSettings.

Loads configuration from environment variables and a local .env file.

Usage:
	from app.config import settings
	settings.MONGODB_URI

This module defines a `Settings` class and a `settings` instance.
"""

from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the application loaded from environment and .env."""

    # MongoDB connection URI (e.g. mongodb://user:pass@host:port)
    MONGODB_URI: str = Field(..., env="MONGODB_URI", description="MongoDB connection URI")

    # Database name to use within the MongoDB server
    DATABASE_NAME: str = Field(..., env="DATABASE_NAME", description="MongoDB database name")

    # Secret key used to sign JWT tokens
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY", description="JWT secret key")

    # Algorithm used for JWT signing (default: HS256)
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM", description="JWT algorithm")

    # Access token lifetime in minutes
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        60,
        env="ACCESS_TOKEN_EXPIRE_MINUTES",
        description="Access token expiration time in minutes",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @field_validator("ACCESS_TOKEN_EXPIRE_MINUTES", mode="before")
    @classmethod
    def _validate_access_token_expire_minutes(cls, value: Any) -> int:
        """Ensure the access token expiry is a positive integer."""
        if isinstance(value, str):
            if not value.isdigit():
                raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be an integer")
            value = int(value)

        if value <= 0:
            raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be greater than 0")

        return value


# Instantiate a singleton settings object for application-wide use.
settings = Settings()
