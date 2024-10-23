from fastapi import FastAPI, Depends, HTTPException, Path
from models import *

from database import engine, SessionLocal
from typing import Annotated

from sqlalchemy.orm import session
from starlette import status

from pydantic import BaseModel



app = FastAPI()


models.Base.metadata.create_all(bind=engine)




def get_db():
    db = SessionLocal
    try:
        yield db
    finally:
        db.close()




db_depensy = Annotated[session, Depends(get_db)]



class TodoRequest():
    title: str
    descreption: str
    priorty: int
    complete: bool



@app.get('/')
def read_all(db: db_depensy):
    return db.query(Todos).all()
    



@app.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
def read_todo(db: db_depensy, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found.')



@app.post('/todo', status_code=status.HTTP_201_CREATED)
def create_todo(db: db_depensy, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.dict())

    db.add(todo_model)
    db.commit()




@app.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def update_todo(db: db_depensy, todo_id: int, todo_request: TodoRequest):
    
    TODO_MODEL = db.query(Todos).filter(Todos.id == todo_id).first()

    if TODO_MODEL is None:
        raise HTTPException(status_code=404, detail='TODO NOT FOUND!!!')

    TODO_MODEL.title = todo_request.title
    TODO_MODEL.descreption = todo_request.descreption
    TODO_MODEL.priorty = todo_request.priorty
    TODO_MODEL.complete = todo_request.complete


    db.add(TODO_MODEL)
    db.commit()