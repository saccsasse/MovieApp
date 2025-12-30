from typing import Optional
from fastapi import Query
from sqlalchemy.orm import Session

from app.db.models.user import User
from app.core.enums import UserRole


def count_admins(db: Session) -> int:
    return db.query(User).filter(User.role == UserRole.ADMIN).count()

def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session) -> list[User]:
    return db.query(User).order_by(User.id).all()

