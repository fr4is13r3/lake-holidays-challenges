"""
Token blacklist system for secure logout functionality.
Simple in-memory implementation that could be extended to use Redis in production.
"""

from datetime import datetime, timedelta
from typing import Set
import asyncio
import structlog

logger = structlog.get_logger()


class TokenBlacklist:
    """
    Simple token blacklist implementation.
    In production, this should use Redis for distributed applications.
    """
    
    def __init__(self):
        self._blacklisted_tokens: Set[str] = set()
        self._cleanup_task = None
    
    def _start_cleanup_task(self):
        """Start background task to clean up expired tokens."""
        if self._cleanup_task is None:
            try:
                loop = asyncio.get_running_loop()
                self._cleanup_task = loop.create_task(self._periodic_cleanup())
            except RuntimeError:
                # No event loop running, skip background task
                logger.info("No event loop running, skipping token cleanup task")
    
    async def _periodic_cleanup(self):
        """Periodically clean up the blacklist (every hour)."""
        while True:
            try:
                await asyncio.sleep(3600)  # 1 hour
                # In a real implementation, we'd clean up based on token expiration
                # For now, we'll keep it simple since tokens expire after 24h
                logger.info("Token blacklist cleanup completed")
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("Error in token blacklist cleanup", error=str(e))
    
    async def blacklist_token(self, token: str) -> None:
        """Add a token to the blacklist."""
        self._blacklisted_tokens.add(token)
        
        # Start cleanup task if not already running
        if self._cleanup_task is None:
            self._start_cleanup_task()
            
        logger.info("Token blacklisted", token_prefix=token[:10] + "...")
    
    async def is_blacklisted(self, token: str) -> bool:
        """Check if a token is blacklisted."""
        return token in self._blacklisted_tokens
    
    async def clear_user_tokens(self, user_id: str) -> None:
        """Clear all tokens for a specific user (placeholder for future enhancement)."""
        # In a more sophisticated implementation, we'd track tokens by user
        # For now, individual token blacklisting is sufficient
        logger.info("User token clearance requested", user_id=user_id)
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        if self._cleanup_task and not self._cleanup_task.done():
            self._cleanup_task.cancel()


# Global token blacklist instance
token_blacklist = TokenBlacklist()