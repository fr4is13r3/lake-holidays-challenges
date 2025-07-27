"""
Challenge service for challenge management operations
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
import structlog
from datetime import datetime

from app.models.challenge import Challenge, ChallengeSubmission, ChallengeType, SubmissionStatus
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
    
    async def submit_quiz_answer(
        self, 
        challenge_id: str, 
        user_id: str, 
        answers: List[int], 
        time_taken: int,
        hints_used: int = 0
    ) -> Dict[str, Any]:
        """
        Submit quiz answers and get immediate feedback.
        
        Args:
            challenge_id: Challenge ID
            user_id: User ID submitting
            answers: List of selected answer indices
            time_taken: Time taken in seconds
            hints_used: Number of hints used
            
        Returns:
            Dict with feedback, correct answers, and points awarded
        """
        challenge = await self.get_challenge_by_id(challenge_id)
        if not challenge or challenge.type != ChallengeType.QUIZ:
            raise ValueError("Invalid quiz challenge")
        
        # Get quiz content
        quiz_content = challenge.content or {}
        questions = quiz_content.get("questions", [])
        
        if len(answers) != len(questions):
            raise ValueError("Number of answers doesn't match number of questions")
        
        # Calculate score
        correct_count = 0
        detailed_results = []
        
        for i, (answer, question) in enumerate(zip(answers, questions)):
            correct_answer = question.get("correct_answer", 0)
            is_correct = answer == correct_answer
            if is_correct:
                correct_count += 1
            
            detailed_results.append({
                "question_index": i,
                "question": question.get("question", ""),
                "selected_answer": answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
                "options": question.get("options", [])
            })
        
        # Calculate points with reductions for hints and time
        base_points = challenge.base_points or 10
        points_per_question = base_points // len(questions) if questions else base_points
        earned_points = correct_count * points_per_question
        
        # Apply hint penalty (50% reduction per hint)
        if hints_used > 0:
            hint_penalty = 0.5 * hints_used
            earned_points = int(earned_points * max(0, 1 - hint_penalty))
        
        # Time bonus/penalty (bonus for quick answers, penalty for very slow)
        time_limit = challenge.content.get("time_limit", 30) * len(questions)
        if time_taken < time_limit * 0.5:  # Very fast
            earned_points = int(earned_points * 1.2)
        elif time_taken > time_limit:  # Over time limit
            earned_points = int(earned_points * 0.8)
        
        # Create submission record
        submission_data = {
            "answers": answers,
            "time_taken": time_taken,
            "hints_used": hints_used,
            "correct_count": correct_count,
            "total_questions": len(questions)
        }
        
        submission = ChallengeSubmission(
            challenge_id=challenge_id,
            user_id=user_id,
            submission_data=submission_data,
            status=SubmissionStatus.APPROVED,  # Auto-approve quiz submissions
            points_awarded=earned_points,
            auto_validated=True,
            validation_score=correct_count / len(questions) if questions else 0,
            submitted_at=datetime.utcnow()
        )
        
        self.db.add(submission)
        await self.db.commit()
        await self.db.refresh(submission)
        
        # Return immediate feedback
        percentage = (correct_count / len(questions) * 100) if questions else 0
        feedback_message = self._generate_feedback_message(percentage, earned_points, hints_used)
        
        return {
            "submission_id": str(submission.id),
            "correct_count": correct_count,
            "total_questions": len(questions),
            "percentage": percentage,
            "points_awarded": earned_points,
            "hints_used": hints_used,
            "time_taken": time_taken,
            "feedback_message": feedback_message,
            "detailed_results": detailed_results
        }
    
    def _generate_feedback_message(self, percentage: float, points: int, hints_used: int) -> str:
        """Generate encouraging feedback message based on performance."""
        if percentage == 100:
            if hints_used == 0:
                return f"Parfait ! Vous avez tout bon sans aide ! +{points} points 🎉"
            else:
                return f"Excellent ! Toutes les bonnes réponses ! +{points} points ⭐"
        elif percentage >= 80:
            return f"Très bien ! {percentage:.0f}% de bonnes réponses. +{points} points 👏"
        elif percentage >= 60:
            return f"Bien joué ! {percentage:.0f}% de réussite. +{points} points 👍"
        elif percentage >= 40:
            return f"Pas mal ! {percentage:.0f}% de bonnes réponses. +{points} points 📚"
        else:
            return f"Continue tes efforts ! {percentage:.0f}% cette fois. +{points} points 💪"
    
    def get_quiz_hint(self, challenge_id: str, question_index: int) -> Optional[str]:
        """Get hint for a specific question in a quiz."""
        # This would be implemented to return hints for questions
        # For now, return a generic hint
        return "Pensez à la culture locale et aux spécialités de La Réunion !"
