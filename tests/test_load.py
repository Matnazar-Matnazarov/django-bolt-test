"""
Load test: req/sec, success/fail counts.

Bolt: uv run manage.py runbolt --dev --host localhost --port 8000
DRF:  uv run manage.py runserver 8001

Then:
    uv run pytest tests/test_load.py -v -m integration
"""

import os
import subprocess
import sys

import pytest


@pytest.mark.integration
def test_load_test_bolt():
    """Run load_test.py against Bolt (runbolt on 8000)."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    result = subprocess.run(
        [sys.executable, "scripts/load_test.py", "-a", "bolt", "-d", "2", "-c", "10"],
        capture_output=True,
        text=True,
        cwd=root,
        timeout=15,
    )
    assert result.returncode == 0, (
        f"Bolt load test failed: {result.stderr or result.stdout}"
    )
    out = result.stdout
    assert "Total requests:" in out and "Requests/sec:" in out


@pytest.mark.integration
def test_load_test_drf():
    """Run load_test.py against DRF (runserver on 8001)."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    result = subprocess.run(
        [
            sys.executable,
            "scripts/load_test.py",
            "-a",
            "drf",
            "-u",
            "http://localhost:8001",
            "-d",
            "2",
            "-c",
            "10",
        ],
        capture_output=True,
        text=True,
        cwd=root,
        timeout=15,
    )
    assert result.returncode == 0, (
        f"DRF load test failed: {result.stderr or result.stdout}"
    )
    out = result.stdout
    assert "Total requests:" in out and "Requests/sec:" in out
