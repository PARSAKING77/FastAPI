from fastapi import FastAPI
from Models import *
from Database import engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)