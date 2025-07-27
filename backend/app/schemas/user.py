from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class UserRole(str, Enum):
    PARENT = "parent"
    CHILD = "child"
    ADMIN = "admin"

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    role: UserRole = UserRole.CHILD

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    role: Optional[UserRole] = None

class User(UserBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# User Profile Schemas
class UserProfileBase(BaseModel):
    display_name: str = Field(..., min_length=1, max_length=100, description="Display name/pseudo for the profile")
    avatar_url: Optional[str] = Field(None, description="Selected avatar from predefined gallery")
    age: Optional[int] = Field(None, ge=1, le=150, description="User age for challenge adaptation")
    challenge_preferences: Optional[dict] = Field(None, description="Challenge type preferences (Sport, Culture, Photo, etc.)")
    bio: Optional[str] = Field(None, max_length=500)

class UserProfileCreate(UserProfileBase):
    display_name: str = Field(..., min_length=1, max_length=100, description="Display name/pseudo (required)")

class UserProfileUpdate(UserProfileBase):
    display_name: Optional[str] = Field(None, min_length=1, max_length=100, description="Display name/pseudo")

class UserProfile(UserProfileBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserWithProfile(User):
    profile: Optional[UserProfile] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: User

class UserResponse(User):
    """Response schema for user data"""
    pass

class UserProfileResponse(UserProfile):
    """Response schema for user profile data"""
    pass