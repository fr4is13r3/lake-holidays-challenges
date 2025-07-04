"""
Authentication endpoints for login, registration, and OAuth
"""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import structlog

from app.database import get_db
from app.models.user import User
from app.schemas.auth import (
    LoginRequest, RegisterRequest, TokenResponse, 
    OAuthRequest, RefreshTokenRequest
)
from app.services.auth_service import AuthService
from app.utils.security import get_current_user

logger = structlog.get_logger()
router = APIRouter()
security = HTTPBearer()


@router.post("/register", response_model=TokenResponse)
async def register(
    request: RegisterRequest,
    req: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user with email and password.
    Creates user account and returns authentication tokens.
    """
    try:
        logger.info("User registration attempt", email=request.email)
        
        # Validate password confirmation
        if request.password != request.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match"
            )
        
        # Check if user already exists
        result = await db.execute(select(User).where(User.email == request.email))
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user through auth service
        auth_service = AuthService(db)
        token_response = await auth_service.register_user(
            email=request.email,
            password=request.password,
            username=request.username,
            ip_address=req.client.host if req.client else None
        )
        
        logger.info("User registered successfully", email=request.email, user_id=token_response.user_id)
        return token_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Registration failed", email=request.email, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    req: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate user with email and password.
    Returns authentication tokens on success.
    """
    try:
        logger.info("User login attempt", email=request.email)
        
        auth_service = AuthService(db)
        token_response = await auth_service.authenticate_user(
            email=request.email,
            password=request.password,
            ip_address=req.client.host if req.client else None
        )
        
        logger.info("User logged in successfully", email=request.email, user_id=token_response.user_id)
        return token_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Login failed", email=request.email, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.post("/oauth/{provider}", response_model=TokenResponse)
async def oauth_login(
    provider: str,
    request: OAuthRequest,
    req: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate user via OAuth (Google or Microsoft).
    Exchanges authorization code for user information and tokens.
    """
    try:
        if provider not in ["google", "microsoft"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported OAuth provider"
            )
        
        logger.info("OAuth login attempt", provider=provider)
        
        auth_service = AuthService(db)
        token_response = await auth_service.oauth_authenticate(
            provider=provider,
            authorization_code=request.code,
            redirect_uri=request.redirect_uri,
            ip_address=req.client.host if req.client else None
        )
        
        logger.info("OAuth login successful", provider=provider, user_id=token_response.user_id)
        return token_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("OAuth login failed", provider=provider, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OAuth authentication failed"
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    Returns new access and refresh tokens.
    """
    try:
        auth_service = AuthService(db)
        token_response = await auth_service.refresh_access_token(request.refresh_token)
        
        logger.info("Token refreshed successfully", user_id=token_response.user_id)
        return token_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Token refresh failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )


@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Logout user and invalidate tokens.
    Adds token to blacklist and clears refresh tokens.
    """
    try:
        auth_service = AuthService(db)
        await auth_service.logout_user(current_user.id, credentials.credentials)
        
        logger.info("User logged out successfully", user_id=current_user.id)
        return {"message": "Logged out successfully"}
        
    except Exception as e:
        logger.error("Logout failed", user_id=current_user.id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )


@router.get("/me")
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user information.
    Returns user details without sensitive data.
    """
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified,
        "oauth_provider": current_user.oauth_provider,
        "created_at": current_user.created_at,
        "last_login": current_user.last_login
    }
