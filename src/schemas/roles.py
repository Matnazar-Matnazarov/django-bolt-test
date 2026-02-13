"""Role schemas."""

from pydantic import BaseModel


class RoleSchema(BaseModel):
    code: str
    name: str
