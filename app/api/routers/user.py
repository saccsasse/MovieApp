from fastapi import APIRouter, Depends, HTTPException, Form
from starlette import status

from app.core.enums import UserRole
from app.core.security import create_access_token, bcrypt_context, Token
from app.db.models.user import User as UserModel
from app.schemas.user import UserCreate, UserOut
from app.api.deps.user import UserDependency
from app.api.deps.db import DbDependency


router = APIRouter(
    prefix="/user",
    tags=["user"]
)


#-------GET-------


@router.get("/me", response_model= UserOut, status_code=status.HTTP_200_OK)
async def read_me(user: UserDependency):
    return UserOut.model_validate(user)


#-------POST-------


@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(db: DbDependency,
                      new_user: UserCreate):

    if db.query(UserModel).filter(UserModel.username == new_user.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists.")
    if db.query(UserModel).filter(UserModel.email == new_user.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists.")

    create_user_model = UserModel(
        username = new_user.username,
        email=new_user.email,
        first_name = new_user.first_name,
        last_name = new_user.last_name,
        hashed_password = bcrypt_context.hash(new_user.password),
        role = UserRole.USER,
        is_active = True
    )

    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return UserOut.model_validate(create_user_model) #Pydantic


@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(
    db: DbDependency,
    username: str = Form(...),
    password: str = Form(...),
):
    db_user = db.query(UserModel).filter(UserModel.username == username).first()

    if not db_user or not bcrypt_context.verify(password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")

    access_token = create_access_token(db_user.username, db_user.id, db_user.role)
    return {"access_token": access_token, "token_type": "bearer"}
