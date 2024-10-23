from fastapi import FastAPI, Depends
from models import *
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import session



app = FastAPI()

models.Base.metadata.create_all(bind=engine)



def get_db():
    db = SessionLocal
    try:
        yield db
    finally:
        db.close()



@app.get('/')
def read_all(db: Annotated[session, Depends(get_db)]):
    return db.query(Todos).all()
    
