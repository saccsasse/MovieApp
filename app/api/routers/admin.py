from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import List

from app.api.services.admin_service import promote_user_to_admin, delete_user

from app.db.repositories.user_repo import get_all_users
from app.db.models.audit import AuditLog

from app.schemas.user import UserOut
from app.schemas.audit import AuditLogOut

from app.api.deps.db import DbDependency
from app.api.deps.user import UserDependency
from app.api.deps.auth import require_role


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_role("ADMIN"))],
)


#--------USERS-------


@router.get("/users", response_model=List[UserOut], status_code=status.HTTP_200_OK)
async def list_users(db: DbDependency):
    users = get_all_users(db)
    return [UserOut.model_validate(u) for u in users]


@router.put("/users/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
async def promote_user(
        db: DbDependency,
        admin: UserDependency,
        user_id: int = Path(...,gt=0)
    ):
    user = promote_user_to_admin(db, admin, user_id)
    return UserOut.model_validate(user)


@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
async def remove_user(
    db: DbDependency,
    admin: UserDependency,
    user_id: int = Path(...,gt=0)
):
    return delete_user(db, admin, user_id)


#--------AUDIT-------


@router.get("/audit-logs", response_model=List[AuditLogOut], status_code=status.HTTP_200_OK)
async def get_audit_log(
        db: DbDependency,
        skip: int = Query(0, ge=0),
        limit: int = Query(50, ge=1, le=500)
):
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()


#--------MOVIES-------










