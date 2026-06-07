"""Authentication request and response schemas."""

from pydantic import BaseModel, EmailStr, Field


class LoginRequestSchema(BaseModel):
    """Request schema for user login."""

    email: EmailStr = Field(
        ..., description="Registered user email address.", example="user@example.com"
    )
    password: str = Field(
        ...,
        description="User password for authentication.",
        example="SecurePass123!",
    )


class TokenResponseSchema(BaseModel):
    """Response schema for JWT access token data."""

    access_token: str = Field(..., description="Signed JWT access token.")
    token_type: str = Field("Bearer", description="Type of token returned.")
