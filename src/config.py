"""Application configuration (env, DB, constants)."""

from __future__ import annotations

import os
from pathlib import Path

# Load .env from project root (same as Django)
_env_path = Path(__file__).resolve().parent.parent / ".env"
if _env_path.exists():
    from dotenv import load_dotenv

    load_dotenv(_env_path)

# Database (same env vars as Django)
DB_NAME = os.getenv("DB_NAME", "bolt_test")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))

# App
APP_PORT = int(os.getenv("FASTAPI_PORT", "8002"))

VALID_ROLES = {"ADMIN", "SHOPKEEPER", "CUSTOMER"}
ROLE_CHOICES = [
    ("ADMIN", "Administrator"),
    ("SHOPKEEPER", "Shopkeeper"),
    ("CUSTOMER", "Customer"),
]
