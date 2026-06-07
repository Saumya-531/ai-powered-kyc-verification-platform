"""User request and response schemas (Pydantic v2).

Defines input validation for registration and the shape of the
returned user object. Uses `ConfigDict(from_attributes=True)` so models
can be populated from ORM-like objects or dicts with attribute access.
"""

from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict


class UserRegisterSchema(BaseModel):
    """Schema for user registration requests.

    Validates name, email, and password. Password and name length
    requirements are enforced via both Field constraints and validators.
    """

    name: str = Field(
        ..., min_length=2, description="Full name of the user.", example="Alice Johnson"
    )
    email: EmailStr = Field(
        ..., description="Email address for user login.", example="alice@example.com"
    )
    password: str = Field(
        ..., min_length=8, description="Secure password with at least 8 characters.", example="StrongPass123!"
    )

    model_config = ConfigDict(from_attributes=True)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        """Normalize and validate the user's name."""
        cleaned = value.strip()
        if len(cleaned) < 2:
            raise ValueError("name must contain at least 2 characters")
        return cleaned

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        """Validate the password meets minimum security requirements."""
        if len(value) < 8:
            raise ValueError("password must contain at least 8 characters")
        return value


class UserResponseSchema(BaseModel):
    """Schema for user data returned in responses.

    `id` is a string representation of the MongoDB ObjectId. Using a
    simple string type keeps response models decoupled from database
    drivers and easy to serialize to JSON.
    """

    id: str = Field(..., description="User identifier (stringified ObjectId)", example="60f7f9a7e13f4b2d9c0e4f1a")
    name: str = Field(..., description="Full name of the user.", example="Alice Johnson")
    email: EmailStr = Field(..., description="Email address of the user.", example="alice@example.com")

    model_config = ConfigDict(from_attributes=True)

