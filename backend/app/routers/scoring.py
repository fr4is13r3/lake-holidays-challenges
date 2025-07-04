"""
Scoring router for points and leaderboard management
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.scoring import ScoreResponse, BadgeResponse, UserBadgeResponse, LeaderboardResponse, UserStats
from app.services.scoring_service import ScoringService
from app.utils.security import get_current_user

router = APIRouter()


@router.post("/award-points", response_model=ScoreResponse)
async def award_points(
    user_id: str,
    season_id: str,
    points: int,
    reason: str,
    challenge_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Award points to a user (admin only)."""
    # In a real implementation, you'd check if current_user is admin
    scoring_service = ScoringService(db)
    score = await scoring_service.award_points(
        user_id=user_id,
        season_id=season_id,
        points=points,
        reason=reason,
        challenge_id=challenge_id
    )
    return score


@router.get("/leaderboard/{season_id}", response_model=LeaderboardResponse)
async def get_season_leaderboard(
    season_id: str,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """Get season leaderboard."""
    # Placeholder implementation
    return {
        "season_id": season_id,
        "season_name": "Season Example",
        "total_participants": 0,
        "entries": [],
        "generated_at": "2025-07-04T12:00:00Z",
        "limit": limit,
        "offset": offset
    }


@router.get("/stats/{user_id}", response_model=UserStats)
async def get_user_stats(
    user_id: str,
    season_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user statistics."""
    # Placeholder implementation
    return {
        "user_id": user_id,
        "season_id": season_id,
        "total_points": 0,
        "season_points": 0,
        "challenges_completed": 0,
        "challenges_attempted": 0,
        "completion_rate": 0.0,
        "badges_earned": 0,
        "rare_badges": 0,
        "current_streak": 0,
        "longest_streak": 0
    }


@router.get("/badges", response_model=List[BadgeResponse])
async def get_available_badges(
    db: AsyncSession = Depends(get_db)
):
    """Get list of available badges."""
    # Placeholder implementation
    return []


@router.get("/my-badges", response_model=List[UserBadgeResponse])
async def get_my_badges(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user's badges."""
    # Placeholder implementation
    return []
