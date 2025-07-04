"""
Season and SeasonMember models
Handles vacation seasons and family group management
"""

import uuid
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Date, Float, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped

from app.database import Base


class Season(Base):
    """
    Holiday season model.
    Represents a vacation period with challenges and participants.
    """
    __tablename__ = "seasons"

    id: Mapped[str] = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Season information
    title: Mapped[str] = Column(String(200), nullable=False)
    description: Mapped[Optional[str]] = Column(Text, nullable=True)
    location: Mapped[str] = Column(String(200), nullable=False)
    
    # Geographic coordinates for AI content generation
    latitude: Mapped[Optional[float]] = Column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = Column(Float, nullable=True)
    
    # Season dates
    start_date: Mapped[date] = Column(Date, nullable=False)
    end_date: Mapped[date] = Column(Date, nullable=False)
    
    # Media
    cover_image_url: Mapped[Optional[str]] = Column(String(500), nullable=True)
    
    # Season limits
    max_members: Mapped[Optional[int]] = Column(Integer, nullable=True)
    
    # Invitation system
    invitation_code: Mapped[str] = Column(String(8), unique=True, nullable=False, index=True)
    
    # Season status
    is_active: Mapped[bool] = Column(Boolean, default=False, nullable=False)
    is_completed: Mapped[bool] = Column(Boolean, default=False, nullable=False)
    
    # Creator
    created_by: Mapped[str] = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    members: Mapped[List["SeasonMember"]] = relationship("SeasonMember", back_populates="season", cascade="all, delete-orphan")
    challenges: Mapped[List["Challenge"]] = relationship("Challenge", back_populates="season", cascade="all, delete-orphan")
    scores: Mapped[List["Score"]] = relationship("Score", back_populates="season", cascade="all, delete-orphan")

    @property
    def is_current(self) -> bool:
        """Check if season is currently active based on dates."""
        today = date.today()
        return self.start_date <= today <= self.end_date

    @property
    def member_count(self) -> int:
        """Get number of active members."""
        try:
            if hasattr(self, 'members') and self.members is not None:
                return len([m for m in self.members if m.is_active])
            return 0
        except Exception:
            # Return 0 if there's any issue accessing members
            return 0

    def __repr__(self):
        return f"<Season {self.title} ({self.start_date} - {self.end_date})>"


class SeasonMember(Base):
    """
    Association table for season membership.
    Tracks who participates in which seasons with roles and status.
    """
    __tablename__ = "season_members"

    id: Mapped[str] = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign keys
    season_id: Mapped[str] = Column(UUID(as_uuid=True), ForeignKey("seasons.id"), nullable=False)
    user_id: Mapped[str] = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Membership info
    role: Mapped[str] = Column(String(20), default="member", nullable=False)  # "creator", "admin", "member"
    nickname: Mapped[Optional[str]] = Column(String(50), nullable=True)  # Nickname for this specific season
    
    # Status
    is_active: Mapped[bool] = Column(Boolean, default=True, nullable=False)
    
    # Participation stats
    total_points: Mapped[int] = Column(Integer, default=0, nullable=False)
    challenges_completed: Mapped[int] = Column(Integer, default=0, nullable=False)
    badges_earned: Mapped[int] = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    joined_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    season: Mapped["Season"] = relationship("Season", back_populates="members")
    user: Mapped["User"] = relationship("User", back_populates="season_memberships")

    def __repr__(self):
        return f"<SeasonMember {self.user_id} in {self.season_id}>"
