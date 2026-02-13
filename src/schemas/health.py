"""Health check schemas."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class HealthTestResponse(BaseModel):
    status: str
    message: str


class ReadyResponse(BaseModel):
    status: str
    checks: dict[str, str]
