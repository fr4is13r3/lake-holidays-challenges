"""
OAuth utilities for Google and Microsoft authentication
"""

import httpx
import json
from typing import Dict, Any, Optional
from urllib.parse import urlencode
import structlog

from app.config import settings

logger = structlog.get_logger()


class OAuthProvider:
    """Base class for OAuth providers."""
    
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.http_client = httpx.AsyncClient()
    
    async def get_user_info(self, authorization_code: str, redirect_uri: str) -> Dict[str, Any]:
        """Exchange authorization code for user info."""
        raise NotImplementedError
    
    async def _exchange_code_for_token(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        """Exchange authorization code for access token."""
        raise NotImplementedError
    
    async def _get_user_profile(self, access_token: str) -> Dict[str, Any]:
        """Get user profile using access token."""
        raise NotImplementedError


class GoogleOAuth(OAuthProvider):
    """Google OAuth implementation."""
    
    def __init__(self):
        super().__init__(
            client_id=getattr(settings, 'google_client_id', ''),
            client_secret=getattr(settings, 'google_client_secret', '')
        )
        self.token_url = "https://oauth2.googleapis.com/token"
        self.user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    
    async def get_user_info(self, authorization_code: str, redirect_uri: str) -> Dict[str, Any]:
        """Get user info from Google OAuth."""
        try:
            # Exchange code for token
            token_data = await self._exchange_code_for_token(authorization_code, redirect_uri)
            access_token = token_data.get("access_token")
            
            if not access_token:
                raise ValueError("No access token received from Google")
            
            # Get user profile
            user_profile = await self._get_user_profile(access_token)
            
            return {
                "id": user_profile.get("id"),
                "email": user_profile.get("email"),
                "username": user_profile.get("name"),
                "first_name": user_profile.get("given_name"),
                "last_name": user_profile.get("family_name"),
                "avatar_url": user_profile.get("picture"),
                "provider": "google"
            }
            
        except Exception as e:
            logger.error("Google OAuth failed", error=str(e))
            raise
    
    async def _exchange_code_for_token(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        """Exchange authorization code for Google access token."""
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        }
        
        response = await self.http_client.post(self.token_url, data=data)
        response.raise_for_status()
        
        return response.json()
    
    async def _get_user_profile(self, access_token: str) -> Dict[str, Any]:
        """Get user profile from Google."""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = await self.http_client.get(self.user_info_url, headers=headers)
        response.raise_for_status()
        
        return response.json()


class MicrosoftOAuth(OAuthProvider):
    """Microsoft OAuth implementation."""
    
    def __init__(self):
        super().__init__(
            client_id=getattr(settings, 'microsoft_client_id', ''),
            client_secret=getattr(settings, 'microsoft_client_secret', '')
        )
        self.token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
        self.user_info_url = "https://graph.microsoft.com/v1.0/me"
    
    async def get_user_info(self, authorization_code: str, redirect_uri: str) -> Dict[str, Any]:
        """Get user info from Microsoft OAuth."""
        try:
            # Exchange code for token
            token_data = await self._exchange_code_for_token(authorization_code, redirect_uri)
            access_token = token_data.get("access_token")
            
            if not access_token:
                raise ValueError("No access token received from Microsoft")
            
            # Get user profile
            user_profile = await self._get_user_profile(access_token)
            
            return {
                "id": user_profile.get("id"),
                "email": user_profile.get("mail") or user_profile.get("userPrincipalName"),
                "username": user_profile.get("displayName"),
                "first_name": user_profile.get("givenName"),
                "last_name": user_profile.get("surname"),
                "provider": "microsoft"
            }
            
        except Exception as e:
            logger.error("Microsoft OAuth failed", error=str(e))
            raise
    
    async def _exchange_code_for_token(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        """Exchange authorization code for Microsoft access token."""
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
            "scope": "openid profile email User.Read",
        }
        
        response = await self.http_client.post(self.token_url, data=data)
        response.raise_for_status()
        
        return response.json()
    
    async def _get_user_profile(self, access_token: str) -> Dict[str, Any]:
        """Get user profile from Microsoft Graph."""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = await self.http_client.get(self.user_info_url, headers=headers)
        response.raise_for_status()
        
        return response.json()


# OAuth URL generators
def get_google_auth_url(redirect_uri: str, state: Optional[str] = None) -> str:
    """Generate Google OAuth authorization URL."""
    params = {
        "client_id": getattr(settings, 'google_client_id', ''),
        "redirect_uri": redirect_uri,
        "scope": "openid profile email",
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent",
    }
    
    if state:
        params["state"] = state
    
    return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"


def get_microsoft_auth_url(redirect_uri: str, state: Optional[str] = None) -> str:
    """Generate Microsoft OAuth authorization URL."""
    params = {
        "client_id": getattr(settings, 'microsoft_client_id', ''),
        "redirect_uri": redirect_uri,
        "scope": "openid profile email User.Read",
        "response_type": "code",
        "response_mode": "query",
    }
    
    if state:
        params["state"] = state
    
    return f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?{urlencode(params)}"
