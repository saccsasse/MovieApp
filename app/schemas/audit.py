from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.schemas.user import UserPublic

class AuditLogOut(BaseModel):

    id: int = Field(...,gt=0, description="An unique AuditLog ID")
    admin_id: int = Field(...,gt=0, description="An unique Admin ID")
    target_user_id: int | None
    action: str = Field(...,min_length=0, max_length=1000, description="Action description")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of action")

    admin: UserPublic
    target_user: Optional[UserPublic] = None

    model_config = {
        "from_attributes": True
    }


