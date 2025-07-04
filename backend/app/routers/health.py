"""
Health check endpoints for monitoring and status
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import structlog

from app.database import get_db
from app.config import settings

logger = structlog.get_logger()
router = APIRouter()


@router.get("/")
async def health_check():
    """
    Basic health check endpoint.
    Returns API status and version.
    """
    return {
        "status": "healthy",
        "version": settings.version,
        "environment": settings.environment,
        "app_name": settings.app_name
    }


@router.get("/ready")
async def readiness_check(db: AsyncSession = Depends(get_db)):
    """
    Readiness check with database connectivity.
    Used by Kubernetes/Docker health checks.
    """
    try:
        # Test database connection
        result = await db.execute(text("SELECT 1"))
        result.scalar()
        
        return {
            "status": "ready",
            "database": "connected",
            "version": settings.version
        }
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        return {
            "status": "not ready",
            "database": "disconnected",
            "error": str(e)
        }


@router.get("/live")
async def liveness_check():
    """
    Liveness check for Kubernetes/Docker.
    Simple endpoint that returns if the app is running.
    """
    return {
        "status": "alive",
        "version": settings.version
    }
