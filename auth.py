from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import session


router = APIRouter()

bcrypt_contaxt = CryptContext(schemes=['bcrypt'], deprecated='auto')



class CreateUserRequest(BaseModel):

    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_depensy = Annotated[session, Depends(get_db)]


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_depensy, create_user_request: CreateUserRequest):

    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed=bcrypt_contaxt.hash(create_user_request.password),
        is_active=True






    )

    
    db.add(create_user_model)
    db.commit()