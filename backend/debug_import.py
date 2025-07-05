#!/usr/bin/env python3
import os
import sys
import traceback

# Set test environment
os.environ["ENVIRONMENT"] = "test"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

print("Python version:", sys.version)
print("Environment:", os.environ.get("ENVIRONMENT"))
print("Database URL:", os.environ.get("DATABASE_URL"))

try:
    print("Importing app.config...")
    from app.config import settings
    print("✓ Config imported successfully")
    print(f"Settings database_url: {settings.database_url}")
    print(f"Settings environment: {settings.environment}")
except Exception as e:
    print(f"✗ Error importing config: {e}")
    traceback.print_exc()

try:
    print("Importing app.database...")
    from app.database import get_database_url, engine
    print("✓ Database imported successfully")
    print(f"Database URL function returns: {get_database_url()}")
except Exception as e:
    print(f"✗ Error importing database: {e}")
    traceback.print_exc()

try:
    print("Importing app.main...")
    from app.main import app
    print("✓ Main app imported successfully")
except Exception as e:
    print(f"✗ Error importing main: {e}")
    traceback.print_exc()

print("Debug complete")
