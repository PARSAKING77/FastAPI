from fastapi import FastAPI, Depends, HTTPException, Request, Form, status  
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm  
from fastapi.templating import Jinja2Templates  
from fastapi.responses import HTMLResponse  
from pydantic import BaseModel  
from typing import List  
from passlib.context import CryptContext  
from fastapi.middleware.cors import CORSMiddleware  
import re 

app = FastAPI()  
templates = Jinja2Templates(directory="Templates")  
origins = ["*"]  

# Middleware  
app.add_middleware(  
    CORSMiddleware,  
    allow_origins=origins,  
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],  
)  

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  

users_db = {}  
todos_db = {}  
current_user_id = None  

def get_password_hash(password):  
    return pwd_context.hash(password)  

def verify_password(plain_password, hashed_password):  
    return pwd_context.verify(plain_password, hashed_password)  

class User(BaseModel):  
    id: int  
    email: str  
    hashed_password: str  

class Todo(BaseModel):  
    id: int  
    name: str  
    description: str  
    complete: bool  

def validate_email(email: str) -> bool:  
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'  
    return re.match(email_regex, email) is not None  







@app.post("/register")  
async def register(email: str = Form(...), password: str = Form(...)):  
    if email in users_db:  
        raise HTTPException(status_code=400, detail="Email already registered.")  
    
    user_id = len(users_db) + 1  
    users_db[email] = User(id=user_id, email=email, hashed_password=get_password_hash(password))  
    return {"message": "User created successfully."}  








@app.post("/login")  
async def login(email: str = Form(...), password: str = Form(...)):  
    for user in users_db.values():  
        if user.email == email and pwd_context.verify(password, user.hashed_password):  
            global current_user_id  
            current_user_id = user.id  # Set the current user  
            return {"detail": "Login successful"}  
    
    raise HTTPException(status_code=401, detail="Invalid email or password")  





@app.post("/logout")  
async def logout():  
    global current_user_id  
    current_user_id = None  
    return {"message": "Logout successful"}  





@app.post("/todos/", response_model=Todo)  
async def create_todo(name: str = Form(...), description: str = Form(...)):  
    if current_user_id is None:  
        raise HTTPException(status_code=401, detail="Not authenticated")  

    todo_id = len(todos_db) + 1  
    todo = Todo(id=todo_id, name=name, description=description, complete=False)  
    todos_db[todo_id] = todo  
    return todo  





@app.put("/todos/{todo_id}")  
async def update_todo(todo_id: int, name: str = Form(...), description: str = Form(...)):  
    if todo_id not in todos_db:  
        raise HTTPException(status_code=404, detail="Todo not found")  

    todos_db[todo_id].name = name  
    todos_db[todo_id].description = description  
    return todos_db[todo_id]  





@app.put("/todos/complete/{todo_id}")  
async def complete_todo(todo_id: int):  
    if current_user_id is None:  
        raise HTTPException(status_code=401, detail="Not authenticated")  

    if todo_id not in todos_db:  
        raise HTTPException(status_code=404, detail="Todo not found")  
    
    todo = todos_db[todo_id]  
    todo.complete = True  
    return todo  




@app.delete("/todos/{todo_id}")  
async def delete_todo(todo_id: int):  
    if current_user_id is None:  
        raise HTTPException(status_code=401, detail="Not authenticated")  

    if todo_id not in todos_db:  
        raise HTTPException(status_code=404, detail="Todo not found")  

    del todos_db[todo_id]  
    return {"message": "Todo deleted successfully"}  




@app.get("/todos/", response_model=List[Todo])  
async def get_todos():  
    if current_user_id is None:  
        raise HTTPException(status_code=401, detail="Not authenticated")  
    return list(todos_db.values())  




@app.get("/users/")  
async def get_users():  
    return list(users_db.values())  




@app.delete("/users/") 
async def delete_user(email: str = Form(...), password: str = Form(...)):  
    global current_user_id  

    user = users_db.get(email)  
    if not user or not verify_password(password, user.hashed_password):  
        raise HTTPException(status_code=401, detail="Invalid email or password")  

    del users_db[email]  
    current_user_id = None  
    return {"message": "User deleted successfully"}