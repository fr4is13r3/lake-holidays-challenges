"""
Scoring, Badge, and UserBadge models
Handles point attribution, leaderboards, and achievement system
"""

import uuid
from datetime import datetime, date
from enum import Enum
from typing import List, Optional
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Boolean, Integer, Date, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped

from app.database import Base


class ScoreType(str, Enum):
    """Types of scoring events."""
    CHALLENGE_COMPLETION = "challenge_completion"
    SPEED_BONUS = "speed_bonus"
    STREAK_BONUS = "streak_bonus"
    TEAM_BONUS = "team_bonus"
    DAILY_BONUS = "daily_bonus"
    PENALTY = "penalty"


class BadgeCategory(str, Enum):
    """Categories of badges."""
    ACHIEVEMENT = "achievement"  # One-time accomplishments
    STREAK = "streak"          # Consecutive activities
    MILESTONE = "milestone"     # Reaching certain numbers
    SPECIAL = "special"        # Special events or perfect scores
    TEAM = "team"             # Team-based achievements


class Score(Base):
    """
    Individual scoring event.
    Tracks all point attributions and deductions.
    """
    __tablename__ = "scores"

    id: Mapped[str] = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign keys
    user_id: Mapped[str] = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    season_id: Mapped[str] = Column(UUID(as_uuid=True), ForeignKey("seasons.id"), nullable=False)
    challenge_id: Mapped[Optional[str]] = Column(UUID(as_uuid=True), ForeignKey("challenges.id"), nullable=True)
    
    # Score details
    points: Mapped[int] = Column(Integer, nullable=False)  # Can be negative for penalties
    score_type: Mapped[ScoreType] = Column(String(30), nullable=False)
    description: Mapped[str] = Column(String(200), nullable=False)
    
    # Context
    score_date: Mapped[date] = Column(Date, default=date.today, nullable=False)
    model_metadata: Mapped[Optional[dict]] = Column(JSON, nullable=True)
    # Example: {"challenge_type": "quiz", "difficulty": "hard", "time_taken": 45, "bonus_reason": "first_correct"}
    
    # Timestamps
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="scores")
    season: Mapped["Season"] = relationship("Season", back_populates="scores")

    def __repr__(self):
        return f"<Score {self.points}pts for {self.user_id} ({self.score_type})>"


class Badge(Base):
    """
    Available badges/achievements.
    Defines all possible achievements users can unlock.
    """
    __tablename__ = "badges"

    id: Mapped[str] = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Badge information
    name: Mapped[str] = Column(String(100), nullable=False, unique=True)
    description: Mapped[str] = Column(Text, nullable=False)
    category: Mapped[BadgeCategory] = Column(String(20), nullable=False)
    
    # Badge appearance
    icon_url: Mapped[Optional[str]] = Column(String(500), nullable=True)
    color: Mapped[str] = Column(String(7), default="#FFD700", nullable=False)  # Hex color
    
    # Unlock criteria
    criteria: Mapped[dict] = Column(JSON, nullable=False)
    # Example: {"type": "challenge_count", "challenge_type": "quiz", "count": 10}
    # Example: {"type": "points_total", "points": 1000}
    # Example: {"type": "streak_days", "days": 7}
    
    # Badge rarity and rewards
    rarity: Mapped[str] = Column(String(20), default="common", nullable=False)  # "common", "rare", "epic", "legendary"
    bonus_points: Mapped[int] = Column(Integer, default=0, nullable=False)  # Points awarded when earned
    
    # Availability
    is_active: Mapped[bool] = Column(Boolean, default=True, nullable=False)
    is_hidden: Mapped[bool] = Column(Boolean, default=False, nullable=False)  # Hidden until earned
    
    # Timestamps
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user_badges: Mapped[List["UserBadge"]] = relationship("UserBadge", back_populates="badge")

    def __repr__(self):
        return f"<Badge {self.name} ({self.category})>"


class UserBadge(Base):
    """
    Badge earned by a user.
    Tracks when and how a user earned each badge.
    """
    __tablename__ = "user_badges"

    id: Mapped[str] = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign keys
    user_id: Mapped[str] = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    badge_id: Mapped[str] = Column(UUID(as_uuid=True), ForeignKey("badges.id"), nullable=False)
    season_id: Mapped[Optional[str]] = Column(UUID(as_uuid=True), ForeignKey("seasons.id"), nullable=True)
    
    # Earning context
    earned_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, nullable=False)
    progress_when_earned: Mapped[Optional[dict]] = Column(JSON, nullable=True)
    # Example: {"challenges_completed": 10, "total_points": 850}
    
    # Display settings
    is_showcased: Mapped[bool] = Column(Boolean, default=False, nullable=False)  # Display on profile
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="user_badges")
    badge: Mapped["Badge"] = relationship("Badge", back_populates="user_badges")

    def __repr__(self):
        return f"<UserBadge {self.user_id} earned {self.badge_id}>"
