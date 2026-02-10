"""Health check routes: /health, /ready."""

from django_bolt.health import add_health_check, register_health_checks
from django.http import HttpRequest


async def check_custom():
    """Optional custom health check (e.g. Redis later)."""
    return True, "OK"


def register(api):
    """Register health endpoints on the given BoltAPI."""
    register_health_checks(api)
    add_health_check(check_custom)
    health_check(api)


def health_check(api):
    """Custom health check endpoint."""

    @api.get("/health/test")
    async def health_test(request: HttpRequest) -> dict:
        """Test health check endpoint."""
        return {"status": "ok", "message": "Test health check endpoint"}
