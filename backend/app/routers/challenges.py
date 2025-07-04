"""
Challenges router for daily challenges management
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.challenge import ChallengeCreate, ChallengeUpdate, ChallengeResponse, ChallengeSubmissionCreate, ChallengeSubmissionResponse
from app.services.challenge_service import ChallengeService
from app.utils.security import get_current_user

router = APIRouter()


@router.post("/", response_model=ChallengeResponse)
async def create_challenge(
    challenge_data: ChallengeCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new challenge."""
    challenge_service = ChallengeService(db)
    challenge = await challenge_service.create_challenge(challenge_data, current_user.id)
    return challenge


@router.get("/{challenge_id}", response_model=ChallengeResponse)
async def get_challenge(
    challenge_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get challenge by ID."""
    challenge_service = ChallengeService(db)
    challenge = await challenge_service.get_challenge_by_id(challenge_id)
    
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge not found"
        )
    
    return challenge


@router.post("/{challenge_id}/submit", response_model=ChallengeSubmissionResponse)
async def submit_challenge(
    challenge_id: str,
    submission_data: ChallengeSubmissionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Submit a challenge response."""
    # This would need to be implemented in ChallengeService
    return {
        "id": "placeholder",
        "challenge_id": challenge_id,
        "user_id": current_user.id,
        "status": "pending",
        "content": submission_data.content,
        "submitted_at": "2025-07-04T12:00:00Z"
    }
