"""Health check routes: /health, /health/test, /ready."""

from fastapi import APIRouter, HTTPException

from src.database import get_pool
from src.schemas.health import HealthResponse, HealthTestResponse, ReadyResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health():
    """Liveness check."""
    return HealthResponse(status="ok")


@router.get("/health/test", response_model=HealthTestResponse)
async def health_test():
    """Custom health check (Bolt-compatible)."""
    return HealthTestResponse(
        status="ok",
        message="Test health check endpoint",
    )


@router.get("/ready", response_model=ReadyResponse)
async def ready():
    """Readiness check (DB). Returns 503 if unhealthy (Bolt-compatible)."""
    try:
        pool = await get_pool()
        async with pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        return ReadyResponse(
            status="healthy",
            checks={"database": "ok"},
        )
    except Exception:
        raise HTTPException(
            status_code=503,
            detail={"status": "unhealthy", "checks": {"database": "error"}},
        )
