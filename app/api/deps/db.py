from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
from app.db.session import get_db

DbDependency = Annotated[Session, Depends(get_db)]