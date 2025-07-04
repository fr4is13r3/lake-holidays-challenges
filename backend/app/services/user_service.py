"""
User service for user management operations
"""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
import structlog

from app.models.user import User, UserProfile
from app.schemas.user import UserCreate, UserUpdate, UserProfileCreate, UserProfileUpdate

logger = structlog.get_logger()


class UserService:
    """Service for user management operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        result = await self.db.execute(
            select(User).options(selectinload(User.profile)).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.db.execute(
            select(User).options(selectinload(User.profile)).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def update_user(self, user_id: str, user_update: UserUpdate) -> Optional[User]:
        """Update user information."""
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def create_user_profile(
        self, user_id: str, profile_data: UserProfileCreate
    ) -> Optional[UserProfile]:
        """Create user profile."""
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        
        # Check if profile already exists
        existing_profile = await self.db.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        if existing_profile.scalar_one_or_none():
            return None  # Profile already exists
        
        profile = UserProfile(
            user_id=user_id,
            **profile_data.model_dump()
        )
        
        self.db.add(profile)
        await self.db.commit()
        await self.db.refresh(profile)
        return profile
    
    async def update_user_profile(
        self, user_id: str, profile_update: UserProfileUpdate
    ) -> Optional[UserProfile]:
        """Update user profile."""
        result = await self.db.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        profile = result.scalar_one_or_none()
        
        if not profile:
            return None
        
        update_data = profile_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(profile, field, value)
        
        await self.db.commit()
        await self.db.refresh(profile)
        return profile
    
    async def deactivate_user(self, user_id: str) -> bool:
        """Deactivate user account."""
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        
        user.is_active = False
        await self.db.commit()
        return True
    
    async def activate_user(self, user_id: str) -> bool:
        """Activate user account."""
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        
        user.is_active = True
        await self.db.commit()
        return True
