from fastapi import FastAPI, Depends, HTTPException, Path, APIRouter
from typing import Annotated
from sqlalchemy.orm import session, sessionmaker
from starlette import status
from pydantic import BaseModel
from .auth import get_current_user
from passlib.context import CryptContext
from models import Todos, Users
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_depensy = Annotated[session, Depends(get_db)]

user_depensy = Annotated[dict, Depends(get_current_user)]

bcrypt_contaxt = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserVerification(BaseModel):
    password: str
    new_password: str





@router.get('/', status_code=status.HTTP_200_OK)
def get_user(user: user_depensy, db: db_depensy):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed!!!')
    return db.query(Users).filter(Users.id == user.get('id')).first()




@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
def change_passwod(user: user_depensy, db: db_depensy, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed!!!')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_contaxt.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Changing Password Failed!!!')

    user_model.hashed_password = bcrypt_contaxt.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
