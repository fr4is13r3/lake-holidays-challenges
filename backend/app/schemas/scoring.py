"""
Scoring and leaderboard schemas for points, badges, and rankings
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class BadgeType(str, Enum):
    ACHIEVEMENT = "achievement"
    MILESTONE = "milestone"
    SPECIAL = "special"
    SEASONAL = "seasonal"


class BadgeRarity(str, Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


# Score Schemas
class ScoreBase(BaseModel):
    points: int = Field(..., ge=0)
    reason: str = Field(..., min_length=1, max_length=200)


class ScoreResponse(ScoreBase):
    id: str
    user_id: str
    season_id: str
    challenge_id: Optional[str] = None
    submission_id: Optional[str] = None
    created_at: datetime
    
    # Additional context
    challenge_title: Optional[str] = None
    season_name: Optional[str] = None
    
    class Config:
        from_attributes = True


# Badge Schemas
class BadgeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    icon_url: Optional[str] = None
    badge_type: BadgeType
    rarity: BadgeRarity = BadgeRarity.COMMON
    points_required: Optional[int] = Field(None, ge=0)
    criteria: Optional[dict] = None


class BadgeResponse(BadgeBase):
    id: str
    created_at: datetime
    
    # Statistics
    users_earned: int = 0
    
    class Config:
        from_attributes = True


# User Badge Schemas
class UserBadgeBase(BaseModel):
    progress: Optional[int] = Field(0, ge=0, le=100)


class UserBadgeResponse(UserBadgeBase):
    id: str
    user_id: str
    badge_id: str
    earned_at: Optional[datetime] = None
    season_id: Optional[str] = None
    
    # Badge details (from join)
    badge_name: Optional[str] = None
    badge_description: Optional[str] = None
    badge_icon_url: Optional[str] = None
    badge_type: Optional[BadgeType] = None
    badge_rarity: Optional[BadgeRarity] = None
    
    class Config:
        from_attributes = True


# Leaderboard Schemas
class LeaderboardEntry(BaseModel):
    rank: int = Field(..., ge=1)
    user_id: str
    total_points: int = Field(..., ge=0)
    challenges_completed: int = Field(..., ge=0)
    badges_earned: int = Field(..., ge=0)
    
    # User details
    user_email: str
    user_first_name: str
    user_last_name: str
    user_avatar_url: Optional[str] = None
    
    # Recent activity
    last_activity: Optional[datetime] = None
    recent_badges: List[UserBadgeResponse] = []


class LeaderboardResponse(BaseModel):
    season_id: str
    season_name: str
    total_participants: int
    entries: List[LeaderboardEntry]
    generated_at: datetime
    
    # Filters applied
    limit: int = 50
    offset: int = 0


class UserStats(BaseModel):
    user_id: str
    season_id: Optional[str] = None
    
    # Points
    total_points: int = 0
    season_points: int = 0
    average_points_per_challenge: Optional[float] = None
    
    # Challenges
    challenges_completed: int = 0
    challenges_attempted: int = 0
    completion_rate: float = 0.0
    
    # Badges
    badges_earned: int = 0
    rare_badges: int = 0
    
    # Rankings
    global_rank: Optional[int] = None
    season_rank: Optional[int] = None
    
    # Activity
    current_streak: int = 0
    longest_streak: int = 0
    last_activity: Optional[datetime] = None


class SeasonStats(BaseModel):
    season_id: str
    season_name: str
    
    # Participation
    total_members: int = 0
    active_members: int = 0
    
    # Challenges
    total_challenges: int = 0
    completed_challenges: int = 0
    
    # Points
    total_points_awarded: int = 0
    average_points_per_member: Optional[float] = None
    
    # Top performers
    top_performer: Optional[LeaderboardEntry] = None
    most_active_day: Optional[datetime] = None
