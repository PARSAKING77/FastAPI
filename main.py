from fastapi import FastAPI, Depends, HTTPException, Path
import models
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import session
from starlette import status
from pydantic import BaseModel
from auth import router  # Correctly import the router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
app.include_router(router)  # Use the imported router directly

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_depensy = Annotated[session, Depends(get_db)]

class TodoRequest(BaseModel):
    title: str
    description: str  # Corrected spelling
    priority: int     # Corrected spelling
    complete: bool

@app.get('/')
def read_all(db: db_depensy):
    return db.query(models.Todos).all()  # Ensure you reference the correct model

@app.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
def read_todo(db: db_depensy, todo_id: int = Path(gt=0)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found.')

@app.post('/todo', status_code=status.HTTP_201_CREATED)
def create_todo(db: db_depensy, todo_request: TodoRequest):
    todo_model = models.Todos(**todo_request.dict())
    db.add(todo_model)
    db.commit()

@app.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def update_todo(db: db_depensy, todo_id: int, todo_request: TodoRequest):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail='TODO NOT FOUND!!!')

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.commit()

@app.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(db: db_depensy, todo_id: int):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail='TODO NOT FOUND!!!')

    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
    db.commit()