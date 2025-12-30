import os

from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from jose import jwt
from pydantic import BaseModel
from dotenv import load_dotenv


"""
in Python Console:
import secrets
random_hex = secrets.token_hex(32)  # 32 bytes, or 64 hex characters
print(random_hex)
"""


load_dotenv()


SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7


if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set")


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(username: str, user_id: int, expires_delta: timedelta | None = None):
    encode = {'sub': username, 'id': user_id, 'type': "access"}
    expires =  datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    encode.update({'exp': expires})
    encoded_jwt = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

