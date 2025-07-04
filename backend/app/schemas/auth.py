"""
Authentication schemas for login, registration, and tokens
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Request schema for user login."""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="User's password")


class RegisterRequest(BaseModel):
    """Request schema for user registration."""
    email: EmailStr = Field(..., description="User's email address")
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Unique username")
    password: str = Field(..., min_length=8, description="User's password")
    confirm_password: str = Field(..., min_length=8, description="Password confirmation")


class Token(BaseModel):
    """JWT token schema."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")


class TokenResponse(BaseModel):
    """Response schema for authentication endpoints."""
    user_id: str = Field(..., description="User's unique identifier")
    email: str = Field(..., description="User's email address")
    username: Optional[str] = Field(None, description="User's username")
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    refresh_token: Optional[str] = Field(None, description="Refresh token for obtaining new access tokens")


class OAuthRequest(BaseModel):
    """OAuth authentication request."""
    provider: str = Field(..., description="OAuth provider (google, microsoft)")
    code: str = Field(..., description="Authorization code from OAuth provider")
    redirect_uri: str = Field(..., description="Redirect URI used in OAuth flow")


class RefreshTokenRequest(BaseModel):
    """Request schema for token refresh."""
    refresh_token: str = Field(..., description="Valid refresh token")


class PasswordResetRequest(BaseModel):
    """Request schema for password reset."""
    email: EmailStr = Field(..., description="User's email address")


class PasswordResetConfirm(BaseModel):
    """Request schema for password reset confirmation."""
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=8, description="New password")
    confirm_password: str = Field(..., min_length=8, description="Password confirmation")
