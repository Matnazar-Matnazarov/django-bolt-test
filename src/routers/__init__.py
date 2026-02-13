"""API routers."""

from fastapi import APIRouter

from src.routers import health, roles, users

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
