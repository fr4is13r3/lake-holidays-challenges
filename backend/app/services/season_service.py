"""
Season service for season management operations
"""

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
    
    async def create_season(self, season_data: SeasonCreate, created_by: str) -> Season:
        """Create a new season."""
        season = Season(
            created_by=created_by,
            **season_data.model_dump()
        )
        
        self.db.add(season)
        await self.db.commit()
        await self.db.refresh(season)
        return season
    
    async def get_season_by_id(self, season_id: str) -> Optional[Season]:
        """Get season by ID."""
        result = await self.db.execute(
            select(Season).where(Season.id == season_id)
        )
        return result.scalar_one_or_none()
    
    async def get_seasons(self, skip: int = 0, limit: int = 50) -> List[Season]:
        """Get list of seasons."""
        result = await self.db.execute(
            select(Season).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
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
