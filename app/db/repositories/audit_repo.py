from typing import Optional

from app.core.celery_app import celery_app
from app.db.session import SessionLocal
from app.db.models.audit import AuditLog


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3})
def log_action_task(self, action: str, admin_id: int, target_user_id: Optional[int] = None):
    db = SessionLocal()
    try:
        log_entry = AuditLog(
            admin_id=admin_id,
            target_user_id=target_user_id,
            action=action,
        )
        db.add(log_entry)

        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise e

    finally:
        db.close()
