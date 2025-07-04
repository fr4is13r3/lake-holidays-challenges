"""
Tests for authentication endpoints
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class TestAuthentication:
    """Test cases for authentication endpoints."""
    
    async def test_register_user(self, client: AsyncClient):
        """Test user registration."""
        user_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "testpassword123",
            "confirm_password": "testpassword123"
        }
        
        response = await client.post("/auth/register", json=user_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "user_id" in data
        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]
    
    async def test_register_user_password_mismatch(self, client: AsyncClient):
        """Test registration with password mismatch."""
        user_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "testpassword123",
            "confirm_password": "differentpassword"
        }
        
        response = await client.post("/auth/register", json=user_data)
        
        assert response.status_code == 400
        assert "Passwords do not match" in response.json()["detail"]
    
    async def test_register_existing_email(self, client: AsyncClient, db_session: AsyncSession):
        """Test registration with existing email."""
        # Create existing user
        from app.utils.security import hash_password
        existing_user = User(
            email="existing@example.com",
            hashed_password=hash_password("password123"),
            is_active=True
        )
        db_session.add(existing_user)
        await db_session.commit()
        
        # Try to register with same email
        user_data = {
            "email": "existing@example.com",
            "username": "newuser",
            "password": "testpassword123",
            "confirm_password": "testpassword123"
        }
        
        response = await client.post("/auth/register", json=user_data)
        
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]
    
    async def test_login_success(self, client: AsyncClient, db_session: AsyncSession):
        """Test successful login."""
        # Create user
        from app.utils.security import hash_password
        user = User(
            email="testuser@example.com",
            hashed_password=hash_password("testpassword123"),
            is_active=True
        )
        db_session.add(user)
        await db_session.commit()
        
        # Login
        login_data = {
            "email": "testuser@example.com",
            "password": "testpassword123"
        }
        
        response = await client.post("/auth/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "user_id" in data
        assert data["email"] == login_data["email"]
    
    async def test_login_wrong_password(self, client: AsyncClient, db_session: AsyncSession):
        """Test login with wrong password."""
        # Create user
        from app.utils.security import hash_password
        user = User(
            email="testuser@example.com",
            hashed_password=hash_password("testpassword123"),
            is_active=True
        )
        db_session.add(user)
        await db_session.commit()
        
        # Login with wrong password
        login_data = {
            "email": "testuser@example.com",
            "password": "wrongpassword"
        }
        
        response = await client.post("/auth/login", json=login_data)
        
        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]
    
    async def test_login_nonexistent_user(self, client: AsyncClient):
        """Test login with non-existent user."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "testpassword123"
        }
        
        response = await client.post("/auth/login", json=login_data)
        
        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]
    
    async def test_get_current_user(self, client: AsyncClient, authenticated_user):
        """Test getting current user information."""
        headers = authenticated_user["headers"]
        
        response = await client.get("/auth/me", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert "email" in data
        assert data["email"] == authenticated_user["user"].email
    
    async def test_get_current_user_no_token(self, client: AsyncClient):
        """Test getting current user without token."""
        response = await client.get("/auth/me")
        
        assert response.status_code == 401
    
    async def test_get_current_user_invalid_token(self, client: AsyncClient):
        """Test getting current user with invalid token."""
        headers = {"Authorization": "Bearer invalid-token"}
        
        response = await client.get("/auth/me", headers=headers)
        
        assert response.status_code == 401
    
    async def test_logout(self, client: AsyncClient, authenticated_user):
        """Test user logout."""
        headers = authenticated_user["headers"]
        
        response = await client.post("/auth/logout", headers=headers)
        
        assert response.status_code == 200
        assert "Logged out successfully" in response.json()["message"]
