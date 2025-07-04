"""
Challenge schemas for challenge management and submissions
"""

from typing import Optional, List, Any, Dict
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl
from enum import Enum


class ChallengeType(str, Enum):
    PHOTO = "photo"
    VIDEO = "video"
    TEXT = "text"
    QUIZ = "quiz"
    LOCATION = "location"
    DRAWING = "drawing"


class ChallengeStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class SubmissionStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"


# Challenge Schemas
class ChallengeBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=1000)
    challenge_type: ChallengeType
    points: int = Field(..., ge=1, le=1000)
    instructions: Optional[str] = Field(None, max_length=2000)
    hints: Optional[List[str]] = None
    media_url: Optional[HttpUrl] = None
    difficulty_level: int = Field(1, ge=1, le=5)
    estimated_duration: Optional[int] = Field(None, ge=1, description="Estimated duration in minutes")


class ChallengeCreate(ChallengeBase):
    season_id: str = Field(..., description="Season ID this challenge belongs to")
    scheduled_date: Optional[datetime] = None


class ChallengeUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    challenge_type: Optional[ChallengeType] = None
    points: Optional[int] = Field(None, ge=1, le=1000)
    instructions: Optional[str] = Field(None, max_length=2000)
    hints: Optional[List[str]] = None
    media_url: Optional[HttpUrl] = None
    difficulty_level: Optional[int] = Field(None, ge=1, le=5)
    estimated_duration: Optional[int] = Field(None, ge=1)
    status: Optional[ChallengeStatus] = None
    scheduled_date: Optional[datetime] = None


class ChallengeResponse(ChallengeBase):
    id: str
    season_id: str
    created_by: str
    status: ChallengeStatus
    order_index: int
    scheduled_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Statistics
    submissions_count: int = 0
    average_rating: Optional[float] = None
    
    class Config:
        from_attributes = True


class ChallengeWithSubmissions(ChallengeResponse):
    submissions: List["ChallengeSubmissionResponse"] = []


# Challenge Submission Schemas
class ChallengeSubmissionBase(BaseModel):
    content: Optional[str] = Field(None, max_length=2000)
    media_urls: Optional[List[HttpUrl]] = None
    metadata: Optional[Dict[str, Any]] = None


class ChallengeSubmissionCreate(ChallengeSubmissionBase):
    challenge_id: str = Field(..., description="Challenge ID for this submission")


class ChallengeSubmissionUpdate(BaseModel):
    content: Optional[str] = Field(None, max_length=2000)
    media_urls: Optional[List[HttpUrl]] = None
    metadata: Optional[Dict[str, Any]] = None


class ChallengeSubmissionResponse(ChallengeSubmissionBase):
    id: str
    challenge_id: str
    user_id: str
    status: SubmissionStatus
    points_awarded: Optional[int] = None
    feedback: Optional[str] = None
    submitted_at: datetime
    reviewed_at: Optional[datetime] = None
    reviewed_by: Optional[str] = None
    
    # User details (from join)
    user_email: Optional[str] = None
    user_first_name: Optional[str] = None
    user_last_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class SubmissionReview(BaseModel):
    submission_id: str
    status: SubmissionStatus
    points_awarded: Optional[int] = Field(None, ge=0)
    feedback: Optional[str] = Field(None, max_length=1000)


class ChallengeStats(BaseModel):
    challenge_id: str
    total_submissions: int
    pending_submissions: int
    approved_submissions: int
    rejected_submissions: int
    average_points: Optional[float] = None
    completion_rate: float = 0.0
