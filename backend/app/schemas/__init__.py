"""
Pydantic schemas for request/response validation
"""

from app.schemas.user import (
    UserCreate, UserLogin, UserResponse, UserUpdate,
    UserProfileCreate, UserProfileUpdate, UserProfileResponse
)
from app.schemas.season import (
    SeasonCreate, SeasonUpdate, SeasonResponse,
    SeasonMemberResponse, SeasonJoinRequest
)
from app.schemas.challenge import (
    ChallengeCreate, ChallengeResponse, ChallengeUpdate,
    ChallengeSubmissionCreate, ChallengeSubmissionResponse
)
from app.schemas.scoring import (
    ScoreResponse, BadgeResponse, UserBadgeResponse,
    LeaderboardResponse, LeaderboardEntry
)
from app.schemas.auth import (
    Token, TokenResponse, LoginRequest, RegisterRequest
)

__all__ = [
    # User schemas
    "UserCreate", "UserLogin", "UserResponse", "UserUpdate",
    "UserProfileCreate", "UserProfileUpdate", "UserProfileResponse",
    
    # Season schemas
    "SeasonCreate", "SeasonUpdate", "SeasonResponse",
    "SeasonMemberResponse", "SeasonJoinRequest",
    
    # Challenge schemas
    "ChallengeCreate", "ChallengeResponse", "ChallengeUpdate",
    "ChallengeSubmissionCreate", "ChallengeSubmissionResponse",
    
    # Scoring schemas
    "ScoreResponse", "BadgeResponse", "UserBadgeResponse",
    "LeaderboardResponse", "LeaderboardEntry",
    
    # Auth schemas
    "Token", "TokenResponse", "LoginRequest", "RegisterRequest",
]
