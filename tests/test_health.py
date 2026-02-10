"""Health check endpoint tests (sync, in-process)."""

import pytest


@pytest.mark.django_db(transaction=True)
def test_health_ok(client):
    """GET /health returns 200 and status ok."""
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "ok"


@pytest.mark.django_db(transaction=True)
def test_health_test(client):
    """GET /health/test returns 200 and custom message."""
    r = client.get("/health/test")
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "ok"
    assert data.get("message") == "Test health check endpoint"


@pytest.mark.django_db(transaction=True)
def test_ready(client):
    """GET /ready returns 200 and status healthy/unhealthy with checks."""
    r = client.get("/ready")
    assert r.status_code == 200
    data = r.json()
    assert "status" in data
    assert data["status"] in ("healthy", "unhealthy")
    assert "checks" in data
