"""
File upload utilities for handling media files
"""

import os
import uuid
import mimetypes
from typing import Optional, List, Tuple
from pathlib import Path
import aiofiles
from fastapi import UploadFile, HTTPException, status
import structlog

from app.config import settings

logger = structlog.get_logger()


class FileUploadHandler:
    """Handler for file uploads with validation and storage."""
    
    def __init__(self):
        self.upload_dir = Path(getattr(settings, 'upload_directory', './uploads'))
        self.max_file_size = getattr(settings, 'max_file_size', 10 * 1024 * 1024)  # 10MB default
        self.allowed_extensions = {
            'image': {'.jpg', '.jpeg', '.png', '.gif', '.webp'},
            'video': {'.mp4', '.webm', '.mov', '.avi'},
            'audio': {'.mp3', '.wav', '.ogg'},
            'document': {'.pdf', '.txt', '.doc', '.docx'}
        }
        
        # Create upload directories
        self._create_directories()
    
    def _create_directories(self):
        """Create upload directories if they don't exist."""
        for category in self.allowed_extensions.keys():
            category_dir = self.upload_dir / category
            category_dir.mkdir(parents=True, exist_ok=True)
    
    def validate_file(self, file: UploadFile) -> Tuple[str, str]:
        """Validate uploaded file and return category and extension."""
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Filename is required"
            )
        
        # Check file size
        if hasattr(file.file, 'seek') and hasattr(file.file, 'tell'):
            file.file.seek(0, 2)  # Seek to end
            size = file.file.tell()
            file.file.seek(0)  # Reset to beginning
            
            if size > self.max_file_size:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"File size exceeds maximum allowed size of {self.max_file_size} bytes"
                )
        
        # Get file extension
        file_ext = Path(file.filename).suffix.lower()
        
        # Determine file category
        category = None
        for cat, extensions in self.allowed_extensions.items():
            if file_ext in extensions:
                category = cat
                break
        
        if not category:
            allowed_exts = set()
            for exts in self.allowed_extensions.values():
                allowed_exts.update(exts)
            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type {file_ext} not allowed. Allowed types: {', '.join(allowed_exts)}"
            )
        
        return category, file_ext
    
    async def save_file(self, file: UploadFile, category: Optional[str] = None) -> dict:
        """Save uploaded file and return file info."""
        try:
            # Validate file
            file_category, file_ext = self.validate_file(file)
            
            # Use provided category or detected category
            if category and category in self.allowed_extensions:
                file_category = category
            
            # Generate unique filename
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            file_path = self.upload_dir / file_category / unique_filename
            
            # Save file
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
            
            # Get file info
            file_info = {
                'filename': file.filename,
                'stored_filename': unique_filename,
                'category': file_category,
                'size': len(content),
                'mime_type': file.content_type or mimetypes.guess_type(file.filename)[0],
                'path': str(file_path),
                'url': f"/uploads/{file_category}/{unique_filename}"
            }
            
            logger.info("File uploaded successfully", **file_info)
            return file_info
            
        except Exception as e:
            logger.error("File upload failed", error=str(e), filename=file.filename)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save file"
            )
    
    async def save_multiple_files(self, files: List[UploadFile], category: Optional[str] = None) -> List[dict]:
        """Save multiple uploaded files."""
        file_infos = []
        
        for file in files:
            file_info = await self.save_file(file, category)
            file_infos.append(file_info)
        
        return file_infos
    
    def delete_file(self, file_path: str) -> bool:
        """Delete a file from storage."""
        try:
            path = Path(file_path)
            if path.exists() and path.is_file():
                path.unlink()
                logger.info("File deleted successfully", path=str(path))
                return True
            else:
                logger.warning("File not found for deletion", path=str(path))
                return False
        except Exception as e:
            logger.error("Failed to delete file", error=str(e), path=file_path)
            return False
    
    def get_file_url(self, category: str, filename: str) -> str:
        """Get URL for uploaded file."""
        return f"/uploads/{category}/{filename}"
    
    def get_file_path(self, category: str, filename: str) -> Path:
        """Get full path for uploaded file."""
        return self.upload_dir / category / filename


# Global instance
file_upload_handler = FileUploadHandler()


# Utility functions
async def upload_single_file(file: UploadFile, category: Optional[str] = None) -> dict:
    """Upload a single file."""
    return await file_upload_handler.save_file(file, category)


async def upload_multiple_files(files: List[UploadFile], category: Optional[str] = None) -> List[dict]:
    """Upload multiple files."""
    return await file_upload_handler.save_multiple_files(files, category)


def delete_uploaded_file(file_path: str) -> bool:
    """Delete an uploaded file."""
    return file_upload_handler.delete_file(file_path)


def get_upload_url(category: str, filename: str) -> str:
    """Get URL for uploaded file."""
    return file_upload_handler.get_file_url(category, filename)
