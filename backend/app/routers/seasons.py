"""
Seasons router for holiday seasons management
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.season import SeasonCreate, SeasonUpdate, SeasonResponse, SeasonJoinRequest, SeasonMemberResponse
from app.services.season_service import SeasonService
from app.utils.security import get_current_user

router = APIRouter()


@router.get("/", response_model=List[SeasonResponse])
async def get_seasons(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get list of seasons."""
    season_service = SeasonService(db)
    seasons = await season_service.get_seasons(skip=skip, limit=limit)
    
    # Convert Season models to SeasonResponse schemas
    season_responses = []
    for season in seasons:
        season_response = SeasonResponse(
            id=str(season.id),
            title=season.title,
            description=season.description,
            location=season.location,
            latitude=season.latitude,
            longitude=season.longitude,
            start_date=season.start_date,
            end_date=season.end_date,
            cover_image_url=season.cover_image_url,
            is_active=season.is_active,
            max_members=season.max_members,
            created_by=str(season.created_by),
            invitation_code=season.invitation_code,
            is_completed=season.is_completed,
            member_count=season.member_count,  # Now safe because relations are loaded
            created_at=season.created_at,
            updated_at=season.updated_at
        )
        season_responses.append(season_response)
    
    return season_responses


@router.post("/", response_model=SeasonResponse)
async def create_season(
    season_data: SeasonCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new season."""
    season_service = SeasonService(db)
    season = await season_service.create_season(season_data, current_user.id)
    
    # Convert to response schema
    return SeasonResponse(
        id=str(season.id),
        title=season.title,
        description=season.description,
        location=season.location,
        latitude=season.latitude,
        longitude=season.longitude,
        start_date=season.start_date,
        end_date=season.end_date,
        cover_image_url=season.cover_image_url,
        is_active=season.is_active,
        max_members=season.max_members,
        created_by=str(season.created_by),
        invitation_code=season.invitation_code,
        is_completed=season.is_completed,
        member_count=season.member_count,
        created_at=season.created_at,
        updated_at=season.updated_at
    )


@router.get("/{season_id}", response_model=SeasonResponse)
async def get_season(
    season_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get season by ID."""
    season_service = SeasonService(db)
    season = await season_service.get_season_by_id(season_id)
    
    if not season:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Season not found"
        )
    
    # Convert to response schema
    return SeasonResponse(
        id=str(season.id),
        title=season.title,
        description=season.description,
        location=season.location,
        latitude=season.latitude,
        longitude=season.longitude,
        start_date=season.start_date,
        end_date=season.end_date,
        cover_image_url=season.cover_image_url,
        is_active=season.is_active,
        max_members=season.max_members,
        created_by=str(season.created_by),
        invitation_code=season.invitation_code,
        is_completed=season.is_completed,
        member_count=season.member_count,
        created_at=season.created_at,
        updated_at=season.updated_at
    )


@router.post("/{season_id}/join", response_model=SeasonMemberResponse)
async def join_season(
    season_id: str,
    join_request: SeasonJoinRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Join a season."""
    season_service = SeasonService(db)
    member = await season_service.join_season(season_id, current_user.id)
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot join season (already member or season not found)"
        )
    
    return member
