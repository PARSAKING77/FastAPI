from fastapi import FastAPI
import models
from database import engine
from auth import router as auth_router
from todos import router as todos_router  

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth_router)  
app.include_router(todos_router)