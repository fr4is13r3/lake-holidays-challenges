"""
Scoring service for points and leaderboard operations
"""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
import structlog

from app.models.scoring import Score, Badge, UserBadge

logger = structlog.get_logger()


class ScoringService:
    """Service for scoring and leaderboard operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def award_points(
        self, user_id: str, season_id: str, points: int, reason: str,
        challenge_id: Optional[str] = None, submission_id: Optional[str] = None
    ) -> Score:
        """Award points to a user."""
        score = Score(
            user_id=user_id,
            season_id=season_id,
            challenge_id=challenge_id,
            submission_id=submission_id,
            points=points,
            reason=reason
        )
        
        self.db.add(score)
        await self.db.commit()
        await self.db.refresh(score)
        return score
