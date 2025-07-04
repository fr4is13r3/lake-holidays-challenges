"""
Geolocation utilities for distance calculation and location services
"""

import math
from typing import Tuple, Optional, Dict, Any
import httpx
import structlog

from app.config import settings

logger = structlog.get_logger()


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth using the Haversine formula.
    
    Args:
        lat1, lon1: Latitude and longitude of first point in decimal degrees
        lat2, lon2: Latitude and longitude of second point in decimal degrees
    
    Returns:
        Distance in kilometers
    """
    # Convert decimal degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = (math.sin(dlat/2)**2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2)
    c = 2 * math.asin(math.sqrt(a))
    
    # Earth's radius in kilometers
    earth_radius = 6371.0
    
    return earth_radius * c


def calculate_distance_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance in meters."""
    return calculate_distance(lat1, lon1, lat2, lon2) * 1000


def is_within_radius(
    center_lat: float, center_lon: float,
    point_lat: float, point_lon: float,
    radius_km: float
) -> bool:
    """Check if a point is within a given radius of a center point."""
    distance = calculate_distance(center_lat, center_lon, point_lat, point_lon)
    return distance <= radius_km


class LocationInfo:
    """Location information container."""
    
    def __init__(self, latitude: float, longitude: float, address: Optional[str] = None,
                 city: Optional[str] = None, country: Optional[str] = None, **kwargs):
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        self.city = city
        self.country = country
        self.extra_data = kwargs
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'address': self.address,
            'city': self.city,
            'country': self.country,
            **self.extra_data
        }


async def get_location_info(latitude: float, longitude: float) -> Optional[LocationInfo]:
    """
    Get location information from coordinates using reverse geocoding.
    This is a simplified implementation - in production, you'd use a real geocoding service.
    """
    try:
        # For now, return basic location info
        # In production, you would call a geocoding API like:
        # - Google Maps Geocoding API
        # - OpenStreetMap Nominatim
        # - MapBox Geocoding API
        
        location_info = LocationInfo(
            latitude=latitude,
            longitude=longitude,
            address=f"Location at {latitude:.6f}, {longitude:.6f}",
            city="Unknown",
            country="Unknown"
        )
        
        logger.info("Location info retrieved", lat=latitude, lon=longitude)
        return location_info
        
    except Exception as e:
        logger.error("Failed to get location info", error=str(e), lat=latitude, lon=longitude)
        return None


async def geocode_address(address: str) -> Optional[LocationInfo]:
    """
    Convert an address to coordinates using geocoding.
    This is a simplified implementation - in production, you'd use a real geocoding service.
    """
    try:
        # For now, return dummy coordinates
        # In production, you would call a geocoding API
        
        location_info = LocationInfo(
            latitude=0.0,
            longitude=0.0,
            address=address,
            city="Unknown",
            country="Unknown"
        )
        
        logger.info("Address geocoded", address=address)
        return location_info
        
    except Exception as e:
        logger.error("Failed to geocode address", error=str(e), address=address)
        return None


class GeofenceChecker:
    """Check if locations are within defined geofences."""
    
    def __init__(self):
        self.geofences = {}
    
    def add_geofence(self, name: str, center_lat: float, center_lon: float, radius_km: float):
        """Add a geofence."""
        self.geofences[name] = {
            'center_lat': center_lat,
            'center_lon': center_lon,
            'radius_km': radius_km
        }
    
    def check_location(self, lat: float, lon: float) -> Dict[str, bool]:
        """Check which geofences contain the given location."""
        results = {}
        
        for name, geofence in self.geofences.items():
            is_inside = is_within_radius(
                geofence['center_lat'], geofence['center_lon'],
                lat, lon,
                geofence['radius_km']
            )
            results[name] = is_inside
        
        return results
    
    def get_nearest_geofence(self, lat: float, lon: float) -> Optional[Tuple[str, float]]:
        """Get the nearest geofence and distance to it."""
        nearest_name = None
        nearest_distance = float('inf')
        
        for name, geofence in self.geofences.items():
            distance = calculate_distance(
                geofence['center_lat'], geofence['center_lon'],
                lat, lon
            )
            
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_name = name
        
        if nearest_name:
            return nearest_name, nearest_distance
        
        return None


# Global geofence checker instance
geofence_checker = GeofenceChecker()


# Utility functions
def validate_coordinates(latitude: float, longitude: float) -> bool:
    """Validate that coordinates are within valid ranges."""
    return -90 <= latitude <= 90 and -180 <= longitude <= 180


def format_coordinates(latitude: float, longitude: float, precision: int = 6) -> str:
    """Format coordinates as a string."""
    return f"{latitude:.{precision}f}, {longitude:.{precision}f}"


def parse_coordinates(coord_string: str) -> Optional[Tuple[float, float]]:
    """Parse coordinates from a string like '45.123456, -73.654321'."""
    try:
        parts = coord_string.split(',')
        if len(parts) != 2:
            return None
        
        lat = float(parts[0].strip())
        lon = float(parts[1].strip())
        
        if validate_coordinates(lat, lon):
            return lat, lon
        
        return None
    except (ValueError, IndexError):
        return None
