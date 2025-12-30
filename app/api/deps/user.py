from typing import Annotated
from fastapi import Depends
from app.db.models.user import User
from app.api.deps.auth import get_current_user

"""
Dependency to inject the currently authenticated user.
Returns the SQLAlchemy User model instance.
"""

UserDependency = Annotated[User, Depends(get_current_user)]
