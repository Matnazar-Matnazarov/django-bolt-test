"""Middleware: X-Server-Time, X-Response-Time (Bolt-compatible)."""

from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class TimingMiddleware(BaseHTTPMiddleware):
    """
    Adds X-Server-Time (UTC) and X-Response-Time (ms) to every response.
    Bolt-compatible observability headers.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        server_time = (
            datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        )
        response.headers["X-Server-Time"] = server_time
        response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"
        return response
