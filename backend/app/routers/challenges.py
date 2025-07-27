"""
Challenges router for daily challenges management
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.database import get_db
from app.models.user import User
from app.schemas.challenge import ChallengeCreate, ChallengeUpdate, ChallengeResponse, ChallengeSubmissionCreate, ChallengeSubmissionResponse
from app.services.challenge_service import ChallengeService
from app.utils.security import get_current_user

router = APIRouter()


class QuizSubmission(BaseModel):
    """Quiz submission data."""
    answers: List[int]
    time_taken: int
    hints_used: int = 0


class QuizResult(BaseModel):
    """Quiz result response."""
    submission_id: str
    correct_count: int
    total_questions: int
    percentage: float
    points_awarded: int
    hints_used: int
    time_taken: int
    feedback_message: str
    detailed_results: List[Dict[str, Any]]


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


@router.post("/{challenge_id}/submit-quiz", response_model=QuizResult)
async def submit_quiz(
    challenge_id: str,
    quiz_data: QuizSubmission,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Submit quiz answers and get immediate feedback."""
    challenge_service = ChallengeService(db)
    
    try:
        result = await challenge_service.submit_quiz_answer(
            challenge_id=challenge_id,
            user_id=current_user.id,
            answers=quiz_data.answers,
            time_taken=quiz_data.time_taken,
            hints_used=quiz_data.hints_used
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{challenge_id}/hint/{question_index}")
async def get_quiz_hint(
    challenge_id: str,
    question_index: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get hint for a specific quiz question."""
    challenge_service = ChallengeService(db)
    hint = challenge_service.get_quiz_hint(challenge_id, question_index)
    
    if not hint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hint not available"
        )
    
    return {"hint": hint}


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
