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
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=500)
    location: str = Field(..., min_length=1, max_length=200)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    start_date: datetime
    end_date: datetime
    cover_image_url: Optional[str] = Field(None, max_length=500)
    is_active: bool = False
    max_members: Optional[int] = Field(None, gt=0)


class SeasonCreate(SeasonBase):
    pass


class SeasonUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=500)
    location: Optional[str] = Field(None, min_length=1, max_length=200)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    cover_image_url: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None
    max_members: Optional[int] = Field(None, gt=0)
    status: Optional[SeasonStatus] = None


class SeasonResponse(SeasonBase):
    id: str
    created_by: str
    invitation_code: str
    is_completed: bool = False
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
