"""User routes: /users, /users/{user_id}."""

from fastapi import APIRouter, HTTPException, Query

from src.config import VALID_ROLES
from src.database import get_pool
from src.schemas.users import UserListResponse, UserSchema

router = APIRouter()


@router.get("", response_model=UserListResponse)
async def list_users(
    search: str | None = Query(None, alias="search"),
    role: str | None = Query(None, alias="role"),
    role_code: str | None = Query(None, alias="role_code"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100, alias="page_size"),
):
    """List users with search and role filter (Bolt-compatible, paginated)."""
    pool = await get_pool()
    role_filter = (role or role_code or "").strip().upper()
    if role_filter and role_filter not in VALID_ROLES:
        role_filter = ""

    conditions = []
    args: list = []
    idx = 1
    if search and search.strip():
        conditions.append(f"username ILIKE ${idx}")
        args.append(f"%{search.strip()}%")
        idx += 1
    if role_filter:
        conditions.append(f"role = ${idx}")
        args.append(role_filter)
        idx += 1

    where_clause = " AND ".join(conditions) if conditions else "1=1"
    offset = (page - 1) * page_size
    args.extend([page_size, offset])

    async with pool.acquire() as conn:
        count_row = await conn.fetchrow(
            f"SELECT COUNT(*)::int as cnt FROM accounts_user WHERE {where_clause}",
            *args[: idx - 1],
        )
        total = count_row["cnt"] if count_row else 0

        rows = await conn.fetch(
            f"""
            SELECT id, username, role FROM accounts_user
            WHERE {where_clause}
            ORDER BY id
            LIMIT ${idx} OFFSET ${idx + 1}
            """,
            *args,
        )

    results = [
        UserSchema(id=r["id"], username=r["username"], role=r["role"] or "CUSTOMER")
        for r in rows
    ]

    next_url = (
        f"?page={page + 1}&page_size={page_size}"
        if (offset + len(results)) < total
        else None
    )
    prev_url = f"?page={page - 1}&page_size={page_size}" if page > 1 else None

    return UserListResponse(
        results=results,
        count=total,
        next=next_url,
        previous=prev_url,
    )


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: int):
    """Get user by ID."""
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT id, username, role FROM accounts_user WHERE id = $1",
            user_id,
        )
    if row is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserSchema(
        id=row["id"],
        username=row["username"],
        role=row["role"] or "CUSTOMER",
    )
