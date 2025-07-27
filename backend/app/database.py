"""
Database configuration and session management
Handles SQLAlchemy async engine and session creation
"""

import os
import sys
import uuid
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import StaticPool
from sqlalchemy import TypeDecorator, String
from sqlalchemy.dialects.postgresql import UUID as PostgreSQL_UUID

from app.config import settings


class UUID(TypeDecorator):
    """Platform-independent UUID type.
    Uses PostgreSQL UUID when possible, otherwise String.
    """
    impl = String
    cache_ok = True
    
    def __init__(self, as_uuid=True):
        self.as_uuid = as_uuid
        super().__init__()

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PostgreSQL_UUID(as_uuid=self.as_uuid))
        else:
            return dialect.type_descriptor(String(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return value
        else:
            return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                return uuid.UUID(value)
            return value


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


def get_database_url():
    """Get the database URL with proper async driver selection."""
    # Check for explicit test environment
    if os.environ.get("ENVIRONMENT") == "test":
        return "sqlite+aiosqlite:///:memory:"
    
    # Check for pytest running (alternative test detection)
    if "pytest" in sys.modules or "PYTEST_CURRENT_TEST" in os.environ:
        return "sqlite+aiosqlite:///:memory:"
    
    # Get the configured database URL
    db_url = settings.database_url
    
    # If DATABASE_URL environment variable is set and points to SQLite, use it
    env_db_url = os.environ.get("DATABASE_URL", "")
    if env_db_url.startswith("sqlite"):
        return env_db_url
    
    # For any PostgreSQL-like URL, ensure we use async driver
    if any(db_url.startswith(prefix) for prefix in ["postgresql://", "postgres://", "postgresql+psycopg2://"]):
        # Extract the URL components and rebuild with asyncpg
        if "://" in db_url:
            scheme, rest = db_url.split("://", 1)
            return f"postgresql+asyncpg://{rest}"
    
    # If it already has the correct async driver, return as-is
    if "+asyncpg://" in db_url or "+aiosqlite://" in db_url:
        return db_url
    
    # Default fallback for testing
    return "sqlite+aiosqlite:///:memory:"


def create_database_engine():
    """Create database engine with appropriate configuration for the database type."""
    db_url = get_database_url()
    
    # SQLite configuration (for testing)
    if db_url.startswith("sqlite"):
        return create_async_engine(
            db_url,
            echo=settings.debug,
            poolclass=StaticPool,
            connect_args={"check_same_thread": False}
        )
    
    # PostgreSQL configuration (for production/development)
    else:
        return create_async_engine(
            db_url,
            echo=settings.debug,  # Log SQL queries in debug mode
            pool_size=20,
            max_overflow=0,
            pool_pre_ping=True,  # Verify connections before use
            pool_recycle=3600,  # Recycle connections every hour
        )


# Create async engine
engine = create_database_engine()

# Create async session maker
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session.
    Used with FastAPI's Depends() for dependency injection.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Initialize database tables."""
    async with engine.begin() as conn:
        # Import all models to ensure they are registered
        from app import models  # noqa: F401
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Close database connections."""
    await engine.dispose()
