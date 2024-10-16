from fastapi import FastAPI


app = FastAPI()

BOOKS = [{"title": "Title One", "author": "Author One", "category": "history"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "math"},
    {"title": "Title Four", "author": "Author Four", "category": "history"},
    {"title": "Title Five", "author": "Author Five", "category": "science"},
    {"title": "Title Six", "author": "Author Two", "category": "math"}
]


@app.get('/books/')
def read_by_category(category: str):
    book_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            book_to_return.append(book)

    return book_to_return