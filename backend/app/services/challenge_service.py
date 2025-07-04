"""
Challenge service for challenge management operations
"""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
import structlog

from app.models.challenge import Challenge, ChallengeSubmission
from app.schemas.challenge import ChallengeCreate, ChallengeUpdate

logger = structlog.get_logger()


class ChallengeService:
    """Service for challenge management operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_challenge(self, challenge_data: ChallengeCreate, created_by: str) -> Challenge:
        """Create a new challenge."""
        challenge = Challenge(
            created_by=created_by,
            **challenge_data.model_dump()
        )
        
        self.db.add(challenge)
        await self.db.commit()
        await self.db.refresh(challenge)
        return challenge
    
    async def get_challenge_by_id(self, challenge_id: str) -> Optional[Challenge]:
        """Get challenge by ID."""
        result = await self.db.execute(
            select(Challenge).where(Challenge.id == challenge_id)
        )
        return result.scalar_one_or_none()
