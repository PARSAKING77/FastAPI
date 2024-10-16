from fastapi import FastAPI


app = FastAPI()

BOOKS = [{"title": "Title One", "author": "Author One", "category": "history"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "math"},
    {"title": "Title Four", "author": "Author Four", "category": "history"},
    {"title": "Title Five", "author": "Author Five", "category": "science"},
    {"title": "Title Six", "author": "Author Two", "category": "math"}
]

@app.post('/book/create_book')

def create_book(new_book):


    BOOKS.append(new_book)