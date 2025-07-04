"""
User and UserProfile models
Handles authentication and user profile information
"""

import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped

from app.database import Base


class User(Base):
    """
    User model for authentication.
    Supports local accounts and OAuth (Google, Microsoft).
    """
    __tablename__ = "users"

    id: Mapped[str] = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = Column(String(255), unique=True, nullable=False, index=True)
    username: Mapped[Optional[str]] = Column(String(50), unique=True, nullable=True, index=True)
    
    # Local authentication
    hashed_password: Mapped[Optional[str]] = Column(String(255), nullable=True)
    
    # OAuth authentication
    oauth_provider: Mapped[Optional[str]] = Column(String(20), nullable=True)  # "google", "microsoft"
    oauth_id: Mapped[Optional[str]] = Column(String(255), nullable=True)
    
    # Account status
    is_active: Mapped[bool] = Column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login: Mapped[Optional[datetime]] = Column(DateTime, nullable=True)
    
    # Relationships
    profile: Mapped[Optional["UserProfile"]] = relationship("UserProfile", back_populates="user", uselist=False)
    season_memberships: Mapped[List["SeasonMember"]] = relationship("SeasonMember", back_populates="user")
    challenge_submissions: Mapped[List["ChallengeSubmission"]] = relationship("ChallengeSubmission", back_populates="user", foreign_keys="[ChallengeSubmission.user_id]")
    scores: Mapped[List["Score"]] = relationship("Score", back_populates="user")
    user_badges: Mapped[List["UserBadge"]] = relationship("UserBadge", back_populates="user")

    def __repr__(self):
        return f"<User {self.email}>"


class UserProfile(Base):
    """
    User profile model for personalization.
    Contains display information and preferences.
    """
    __tablename__ = "user_profiles"

    id: Mapped[str] = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[str] = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    
    # Profile information
    display_name: Mapped[str] = Column(String(100), nullable=False)
    avatar_url: Mapped[Optional[str]] = Column(String(500), nullable=True)
    bio: Mapped[Optional[str]] = Column(Text, nullable=True)
    
    # Demographics
    age: Mapped[Optional[int]] = Column(Integer, nullable=True)
    
    # Preferences for challenge generation
    challenge_preferences: Mapped[Optional[dict]] = Column(JSON, nullable=True, default=dict)
    # Example: {"sport": True, "culture": True, "photo": True, "difficulty": "medium"}
    
    # Location preferences
    timezone: Mapped[Optional[str]] = Column(String(50), nullable=True, default="UTC")
    language: Mapped[str] = Column(String(10), nullable=False, default="fr")
    
    # Privacy settings
    is_profile_public: Mapped[bool] = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<UserProfile {self.display_name}>"
