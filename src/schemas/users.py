"""User schemas."""

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str
    role: str


class UserListResponse(BaseModel):
    results: list[UserSchema]
    count: int
    next: str | None = None
    previous: str | None = None
