"""
Authentication service for user management and JWT tokens
"""

import uuid
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status
import structlog

from app.config import settings
from app.models.user import User
from app.schemas.auth import TokenResponse
from app.utils.oauth import GoogleOAuth, MicrosoftOAuth

logger = structlog.get_logger()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Service for authentication and user management."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.google_oauth = GoogleOAuth()
        self.microsoft_oauth = MicrosoftOAuth()
    
    async def register_user(
        self,
        email: str,
        password: str,
        username: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> TokenResponse:
        """Register a new user with email and password."""
        
        # Hash password
        hashed_password = self._hash_password(password)
        
        # Create user
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
            is_active=True,
            is_verified=False,  # Email verification required
            last_login=datetime.utcnow()
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        # Generate tokens
        return await self._generate_token_response(user)
    
    async def authenticate_user(
        self,
        email: str,
        password: str,
        ip_address: Optional[str] = None
    ) -> TokenResponse:
        """Authenticate user with email and password."""
        
        # Get user by email
        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        
        if not user or not user.hashed_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Verify password
        if not self._verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is deactivated"
            )
        
        # Update last login
        user.last_login = datetime.utcnow()
        await self.db.commit()
        
        # Generate tokens
        return await self._generate_token_response(user)
    
    async def oauth_authenticate(
        self,
        provider: str,
        authorization_code: str,
        redirect_uri: str,
        ip_address: Optional[str] = None
    ) -> TokenResponse:
        """Authenticate user via OAuth provider."""
        
        # Get OAuth client
        if provider == "google":
            oauth_client = self.google_oauth
        elif provider == "microsoft":
            oauth_client = self.microsoft_oauth
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported OAuth provider"
            )
        
        # Exchange code for user info
        try:
            user_info = await oauth_client.get_user_info(authorization_code, redirect_uri)
        except Exception as e:
            logger.error("OAuth authentication failed", provider=provider, error=str(e))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="OAuth authentication failed"
            )
        
        # Find or create user
        result = await self.db.execute(select(User).where(User.email == user_info["email"]))
        user = result.scalar_one_or_none()
        
        if user:
            # Update OAuth info for existing user
            user.oauth_provider = provider
            user.oauth_id = user_info["id"]
            user.last_login = datetime.utcnow()
        else:
            # Create new user
            user = User(
                email=user_info["email"],
                username=user_info.get("username"),
                oauth_provider=provider,
                oauth_id=user_info["id"],
                is_active=True,
                is_verified=True,  # OAuth users are considered verified
                last_login=datetime.utcnow()
            )
            self.db.add(user)
        
        await self.db.commit()
        await self.db.refresh(user)
        
        # Generate tokens
        return await self._generate_token_response(user)
    
    async def refresh_access_token(self, refresh_token: str) -> TokenResponse:
        """Refresh access token using refresh token."""
        
        try:
            payload = jwt.decode(
                refresh_token,
                settings.secret_key,
                algorithms=[settings.algorithm]
            )
            user_id = payload.get("sub")
            token_type = payload.get("type")
            
            if token_type != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token type"
                )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Get user
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Generate new tokens
        return await self._generate_token_response(user)
    
    async def logout_user(self, user_id: str, access_token: str):
        """Logout user and invalidate tokens."""
        # In a production system, you would:
        # 1. Add the token to a blacklist/redis cache
        # 2. Remove refresh tokens from database
        # This is a simplified implementation
        logger.info("User logged out", user_id=user_id)
    
    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt."""
        return pwd_context.hash(password)
    
    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    async def _generate_token_response(self, user: User) -> TokenResponse:
        """Generate JWT tokens for user."""
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = self._create_token(
            data={"sub": str(user.id), "type": "access"},
            expires_delta=access_token_expires
        )
        
        # Create refresh token
        refresh_token_expires = timedelta(days=settings.refresh_token_expire_days)
        refresh_token = self._create_token(
            data={"sub": str(user.id), "type": "refresh"},
            expires_delta=refresh_token_expires
        )
        
        return TokenResponse(
            user_id=str(user.id),
            email=user.email,
            username=user.username,
            access_token=access_token,
            token_type="bearer",
            expires_in=int(access_token_expires.total_seconds()),
            refresh_token=refresh_token
        )
    
    def _create_token(self, data: dict, expires_delta: timedelta) -> str:
        """Create JWT token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        
        return jwt.encode(
            to_encode,
            settings.secret_key,
            algorithm=settings.algorithm
        )
