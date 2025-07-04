"""
AI Content router for AI-powered features
"""

from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.services.ai_service import AIService
from app.utils.security import get_current_user

router = APIRouter()


@router.post("/generate-challenge")
async def generate_challenge_content(
    theme: str,
    difficulty: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """Generate challenge content using AI."""
    if difficulty < 1 or difficulty > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Difficulty must be between 1 and 5"
        )
    
    ai_service = AIService()
    content = await ai_service.generate_challenge_content(theme, difficulty)
    return content


@router.post("/analyze-submission")
async def analyze_submission(
    submission_content: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """Analyze submission content using AI."""
    if not submission_content.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Submission content cannot be empty"
        )
    
    ai_service = AIService()
    analysis = await ai_service.analyze_submission(submission_content)
    return analysis


@router.get("/suggestions")
async def get_challenge_suggestions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """Get AI-generated challenge suggestions."""
    # Placeholder implementation
    return {
        "suggestions": [
            {
                "theme": "Nature",
                "difficulty": 2,
                "description": "Trouve un objet naturel intéressant et raconte son histoire"
            },
            {
                "theme": "Créativité",
                "difficulty": 3,
                "description": "Crée quelque chose de nouveau avec des objets du quotidien"
            },
            {
                "theme": "Mouvement",
                "difficulty": 1,
                "description": "Apprends un nouveau geste ou mouvement"
            }
        ]
    }


@router.post("/personalized-content")
async def get_personalized_content(
    user_preferences: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """Get personalized content based on user preferences."""
    # Placeholder implementation
    return {
        "personalized_challenges": [],
        "recommended_themes": ["Nature", "Art", "Sport"],
        "difficulty_recommendation": 2,
        "motivational_message": f"Salut {current_user.first_name}, prêt pour de nouveaux défis ?"
    }
