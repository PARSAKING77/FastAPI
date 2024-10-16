from fastapi import FastAPI

app = FastAPI()

BOOKS = [{"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "science"},
    {"title": "Title Four", "author": "Author Four", "category": "history"},
    {"title": "Title Five", "author": "Author Five", "category": "science"},
    {"title": "Title Six", "author": "Author Two", "category": "math"}
]

@app.delete('/del')

def delete_book(book_title: str):
    for x in range(len(BOOKS)):
        if BOOKS[x].get('title').casefold() == book_title.casefold():
            break