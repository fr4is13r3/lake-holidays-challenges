"""
Database models for Lake Holidays Challenge
"""

from app.models.user import User, UserProfile
from app.models.season import Season, SeasonMember  
from app.models.challenge import Challenge, ChallengeSubmission, ChallengeType
from app.models.scoring import Score, Badge, UserBadge

__all__ = [
    "User",
    "UserProfile", 
    "Season",
    "SeasonMember",
    "Challenge",
    "ChallengeSubmission",
    "ChallengeType",
    "Score",
    "Badge",
    "UserBadge",
]
