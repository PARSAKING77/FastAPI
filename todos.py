from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Annotated
from sqlalchemy.orm import session
from starlette import status
from pydantic import BaseModel
from models import Todos
from .auth import get_current_user
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str
    description: str  
    priority: int     
    complete: bool

@router.get('/')
def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed!!!')

    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

@router.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    
    if todo_model is not None:
    
        return todo_model

    raise HTTPException(status_code=404, detail='Todo not found!!!')



@router.post('/todo', status_code=status.HTTP_201_CREATED)
def create_todo(user: user_depensy, db: db_depensy, todo_request: TodoRequest):

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed!!!')

    todo_model = models.Todos(**todo_request.dict(), owner_id=user.get('id'))

    db.add(todo_model)
    db.commit()

@router.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def update_todo(user: user_depensy, db: db_depensy, todo_id: int, todo_request: TodoRequest):

    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed!!!')

    if todo_model is None:
        raise HTTPException(status_code=404, detail='TODO NOT FOUND!!!')

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.commit()

@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(user: user_depensy, db: db_depensy, todo_id: int):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed!!!')

    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).filetr(Todos.owner_id == user.get('id')).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail='TODO NOT FOUND!!!')

    db.query(models.Todos).filter(models.Todos.id == todo_id).filetr(Todos.owner_id == user.get('id')).delete()
    db.commit()
