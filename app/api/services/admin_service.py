import logging

from fastapi import HTTPException, Query
from starlette import status

from app.db.repositories.user_repo import get_user_by_id, count_admins
from app.db.repositories.audit_repo import log_action_task
from app.db.models.user import User
from app.core.enums import UserRole, AuditAction
from app.api.deps.db import DbDependency


def promote_user_to_admin(db: DbDependency, admin: User, user_id_to_promote: int) -> User:
    user_to_promote = get_user_by_id(db, user_id_to_promote)
    if not user_to_promote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_to_promote.role = UserRole.ADMIN
    db.commit()

    logging.info(f"Admin {admin.id} promoted user {user_to_promote.id} to admin role")
    log_action_task.delay(
        action=AuditAction.PROMOTE_USER.value,
        admin_id=admin.id,
        target_user_id=user_to_promote.id,
    )
    return user_to_promote


def delete_user(db: DbDependency, admin: User, user_id_to_delete: int):
    user_to_delete = get_user_by_id(db, user_id_to_delete)
    if not user_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    #protect last admin
    if user_to_delete.role == UserRole.ADMIN and count_admins(db) == 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete last admin")

    db.delete(user_to_delete)
    db.commit()

    logging.info(f"Admin {admin.id} deleted user {user_to_delete.id}")
    log_action_task.delay(
        action=AuditAction.DELETE_USER.value,
        admin_id=admin.id,
        target_user_id=user_to_delete.id,
    )
    return {"msg": "User deleted successfully"}
