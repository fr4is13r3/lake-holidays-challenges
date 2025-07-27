"""
Tests for session management functionality (US003)
"""

import pytest
from datetime import datetime, timedelta
from jose import jwt

from app.config import settings
from app.services.auth_service import AuthService
from app.utils.token_blacklist import token_blacklist


class TestSessionManagement:
    """Test cases for user session management."""
    
    async def test_24_hour_session_duration(self):
        """Test that access tokens are valid for 24 hours minimum."""
        # Verify configuration is set for 24h sessions
        assert settings.access_token_expire_minutes >= 1440  # 24 hours
        
        # Create a test token
        test_data = {"sub": "test-user-id", "type": "access"}
        
        # Create token with default expiration
        auth_service = AuthService(None)  # DB not needed for token creation
        token = auth_service._create_token(
            data=test_data,
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
        )
        
        # Decode token to check expiration
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        exp_timestamp = payload.get("exp")
        
        # Calculate time difference
        exp_datetime = datetime.utcfromtimestamp(exp_timestamp)
        now = datetime.utcnow()
        time_diff = exp_datetime - now
        
        # Should be at least 24 hours (allowing for small test execution time)
        assert time_diff.total_seconds() >= 86400 - 60  # 24 hours minus 1 minute buffer
    
    async def test_token_blacklist_on_logout(self):
        """Test that tokens are properly blacklisted on logout."""
        test_token = "test-token-123"
        
        # Token should not be blacklisted initially
        assert not await token_blacklist.is_blacklisted(test_token)
        
        # Blacklist the token
        await token_blacklist.blacklist_token(test_token)
        
        # Token should now be blacklisted
        assert await token_blacklist.is_blacklisted(test_token)
    
    async def test_refresh_token_duration(self):
        """Test that refresh tokens are valid for 7 days minimum."""
        # Verify configuration
        assert settings.refresh_token_expire_days >= 7
        
        # Create a test refresh token
        test_data = {"sub": "test-user-id", "type": "refresh"}
        
        auth_service = AuthService(None)
        token = auth_service._create_token(
            data=test_data,
            expires_delta=timedelta(days=settings.refresh_token_expire_days)
        )
        
        # Decode token to check expiration
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        exp_timestamp = payload.get("exp")
        
        # Calculate time difference
        exp_datetime = datetime.utcfromtimestamp(exp_timestamp)
        now = datetime.utcnow()
        time_diff = exp_datetime - now
        
        # Should be at least 7 days
        assert time_diff.total_seconds() >= 7 * 86400 - 60  # 7 days minus buffer