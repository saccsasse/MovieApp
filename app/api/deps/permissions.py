from typing import Annotated
from fastapi import Depends
from app.api.deps.auth import require_role
from app.db.models.user import User

AdminUser = Annotated[User, Depends(require_role("ADMIN"))]
