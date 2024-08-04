from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from models import Users
from database import SessionLocal
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user, update_password

router = APIRouter(prefix="/users", tags=["users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class ChangePwdRequest(BaseModel):
    current_password: str = Field()
    new_password: str = Field(min_length=6)


@router.get("/get_user", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_model is not None:
        return user_model
    raise HTTPException(status_code=404, detail="User found")


@router.put("/change_password", status_code=status.HTTP_200_OK)
async def change_password(
    user: user_dependency, db: db_dependency, change_pwd_request: ChangePwdRequest
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    isUpdated = update_password(
        user.get("username"),
        change_pwd_request.current_password,
        change_pwd_request.new_password,
        db,
    )
    if not isUpdated:
        raise HTTPException(status_code=401, detail="Authentication Failed")


@router.put(
    "/change_phone_number/{phone_number}", status_code=status.HTTP_204_NO_CONTENT
)
async def change_phone_number(
    user: user_dependency, db: db_dependency, phone_number: str
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
