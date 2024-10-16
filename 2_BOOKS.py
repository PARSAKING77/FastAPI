from fastapi import FastAPI

app = FastAPI()

BOOKS = [{"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "science"},
    {"title": "Title Four", "author": "Author Four", "category": "history"},
    {"title": "Title Five", "author": "Author Five", "category": "science"},
    {"title": "Title Six", "author": "Author Two", "category": "math"}
]

@app.get('/')
def first():
    return BOOKS