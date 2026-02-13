"""Role routes: /roles, /roles/code/{code}."""

from fastapi import APIRouter, HTTPException

from src.config import ROLE_CHOICES
from src.schemas.roles import RoleSchema

router = APIRouter()


@router.get("", response_model=list[RoleSchema])
async def list_roles():
    """List all roles (Bolt-compatible)."""
    return [RoleSchema(code=c, name=n) for c, n in ROLE_CHOICES]


@router.get("/code/{code}", response_model=RoleSchema)
async def get_role_by_code(code: str):
    """Get role by code."""
    code_upper = (code or "").strip().upper()
    for c, n in ROLE_CHOICES:
        if c == code_upper:
            return RoleSchema(code=c, name=n)
    raise HTTPException(status_code=404, detail="Role not found")
