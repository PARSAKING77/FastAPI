from fastapi import FastAPI, Depends, HTTPException, Path, APIRouter
from typing import Annotated
from sqlalchemy.orm import session, sessionmaker
from starlette import status
from pydantic import BaseModel
from .auth import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_depensy = Annotated[session, Depends(get_db)]

user_depensy = Annotated[dict, Depends(get_current_user)]


@rouetr.get('/todos', status_code=status.HTTP_200_OK)
def read_all(user: user_depensy, db: db_depensy):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed!!!')

    return db.query(Todos).all()


@router.delete('/todos/{todos_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(user: user_depensy, db: db_depensy, todo_id: int):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed!!!')
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail='TODO NOT FOUND!!!')

    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
    db.commit()