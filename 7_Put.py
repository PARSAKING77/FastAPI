from fastapi import FastAPI
import Body

app = FastAPI()

BOOKS = [{"title": "Title One", "author": "Author One", "category": "history"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "math"},
    {"title": "Title Four", "author": "Author Four", "category": "history"},
    {"title": "Title Five", "author": "Author Five", "category": "science"},
    {"title": "Title Six", "author": "Author Two", "category": "math"}
]

@app.put('/book/updated_book')

def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book