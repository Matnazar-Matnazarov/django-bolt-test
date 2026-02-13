"""
FastAPI application (Bolt-compatible).

Same endpoints as Django Bolt: /health, /health/test, /ready, /roles, /users.
Uses asyncpg, uvloop (auto when installed). X-Server-Time, X-Response-Time on every response.

Usage:
    uv run uvicorn src.main:app --host 0.0.0.0 --port 8002
    uv run uvicorn src.main:app --host 0.0.0.0 --port 8002 --workers 4  # load test
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import APP_PORT
from src.database import close_pool
from src.middleware import TimingMiddleware
from src.routers import api_router
import uvloop
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await close_pool()


app = FastAPI(
    title="FastAPI (Bolt-compatible)",
    description="Same endpoints as Django Bolt. X-Server-Time, X-Response-Time on every response.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(TimingMiddleware)
app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    # uvloop is used automatically by uvicorn when installed
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=APP_PORT,
        reload=True,
    )
