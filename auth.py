from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta


router = APIRouter()

secret = 'ef782a0263b154fd337fb3cb4134a1e740f2dbb381bc7b200a09ab88bca97f0f'
algorithm1 = 'HS256'

bcrypt_contaxt = CryptContext(schemes=['bcrypt'], deprecated='auto')


oauth2_baerer = OAuth2PasswordBearer(tokenUrl='token')

class CreateUserRequest(BaseModel):

    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str





def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_depensy = Annotated[session, Depends(get_db)]



def authenticate_user(user: str, password: str, db):
    user = db.query(Users).filter(User.username == username).first()

    if not user:
        return False
    if not bcrypt_contaxt.verify(password, user.hashed):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):

    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta

    encode.update({'exp': expires})
    

    return jwt.encode(encode, secret, algorithm=algorithm1)


def get_current_user(token: Annotated[str, Depends(oauth2_baerer)]):
    
    try:
        paylod = jwt.decode(token, secret, algorithms=[algorithm1])
        username: str = paylod.get('sub')
        user_id: int = paylod.get('id')

        if username is not None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
        
        return {'username': username, 'id': user_id}
    except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
 
    




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




@router.post('/token', response_model=Token)
def login_for_access_token(from_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_depensy):

    user = authenticate_user(from_data.username, from_data.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')



    token1 = create_access_token(user.username, user.id, timedelta(minutes=20))


    return {'access_token': token1, 'token_type': 'bearer'}



