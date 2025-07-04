"""
Season service for season management operations
"""

import uuid
import secrets
import string
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload
import structlog

from app.models.season import Season, SeasonMember
from app.schemas.season import SeasonCreate, SeasonUpdate

logger = structlog.get_logger()


class SeasonService:
    """Service for season management operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    def _generate_invitation_code(self) -> str:
        """Generate a unique 6-character invitation code."""
        return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    
    async def create_season(self, season_data: SeasonCreate, created_by: str) -> Season:
        """Create a new season."""
        # Generate unique invitation code
        invitation_code = self._generate_invitation_code()
        
        # Ensure invitation code is unique
        while True:
            result = await self.db.execute(
                select(Season).where(Season.invitation_code == invitation_code)
            )
            if not result.scalar_one_or_none():
                break
            invitation_code = self._generate_invitation_code()
        
        # Convert datetime to date for start_date and end_date
        start_date = season_data.start_date.date() if hasattr(season_data.start_date, 'date') else season_data.start_date
        end_date = season_data.end_date.date() if hasattr(season_data.end_date, 'date') else season_data.end_date
        
        season = Season(
            title=season_data.title,
            description=season_data.description,
            location=season_data.location,
            latitude=season_data.latitude,
            longitude=season_data.longitude,
            start_date=start_date,
            end_date=end_date,
            cover_image_url=season_data.cover_image_url,
            max_members=season_data.max_members,
            invitation_code=invitation_code,
            is_active=season_data.is_active,
            created_by=created_by
        )
        
        self.db.add(season)
        await self.db.commit()
        await self.db.refresh(season)
        
        # Automatically add the creator as an admin member
        creator_member = SeasonMember(
            season_id=season.id,
            user_id=created_by,
            role="admin"
        )
        self.db.add(creator_member)
        await self.db.commit()
        
        return season
    
    async def get_season_by_id(self, season_id: str) -> Optional[Season]:
        """Get season by ID with relationships loaded."""
        result = await self.db.execute(
            select(Season)
            .options(selectinload(Season.members))
            .where(Season.id == season_id)
        )
        return result.scalar_one_or_none()
    
    async def get_seasons(self, skip: int = 0, limit: int = 50) -> List[Season]:
        """Get list of seasons with relationships loaded."""
        result = await self.db.execute(
            select(Season)
            .options(selectinload(Season.members))
            .offset(skip)
            .limit(limit)
            .order_by(Season.created_at.desc())
        )
        return list(result.scalars().all())
    
    async def join_season(self, season_id: str, user_id: str) -> Optional[SeasonMember]:
        """Join a user to a season."""
        season = await self.get_season_by_id(season_id)
        if not season:
            return None
        
        # Check if already a member
        existing = await self.db.execute(
            select(SeasonMember).where(
                and_(SeasonMember.season_id == season_id, SeasonMember.user_id == user_id)
            )
        )
        if existing.scalar_one_or_none():
            return None
        
        member = SeasonMember(season_id=season_id, user_id=user_id)
        self.db.add(member)
        await self.db.commit()
        await self.db.refresh(member)
        return member
