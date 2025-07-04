"""
Season schemas for season management and member operations
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class SeasonStatus(str, Enum):
    UPCOMING = "upcoming"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class SeasonMemberRole(str, Enum):
    MEMBER = "member"
    MODERATOR = "moderator"
    ADMIN = "admin"


# Season Schemas
class SeasonBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    start_date: datetime
    end_date: datetime
    is_public: bool = True
    max_members: Optional[int] = Field(None, gt=0)


class SeasonCreate(SeasonBase):
    pass


class SeasonUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_public: Optional[bool] = None
    max_members: Optional[int] = Field(None, gt=0)
    status: Optional[SeasonStatus] = None


class SeasonResponse(SeasonBase):
    id: str
    created_by: str
    status: SeasonStatus
    member_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class SeasonWithDetails(SeasonResponse):
    challenges_count: int = 0
    total_points: int = 0


# Season Member Schemas
class SeasonMemberBase(BaseModel):
    role: SeasonMemberRole = SeasonMemberRole.MEMBER


class SeasonJoinRequest(BaseModel):
    season_id: str = Field(..., description="Season ID to join")
    message: Optional[str] = Field(None, max_length=200, description="Optional join message")


class SeasonMemberResponse(SeasonMemberBase):
    id: str
    season_id: str
    user_id: str
    joined_at: datetime
    points: int = 0
    
    # User details (from join)
    user_email: Optional[str] = None
    user_first_name: Optional[str] = None
    user_last_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class SeasonLeaderboard(BaseModel):
    season_id: str
    members: List[SeasonMemberResponse]
    total_members: int
