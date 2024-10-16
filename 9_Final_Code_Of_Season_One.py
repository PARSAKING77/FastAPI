from fastapi import FastAPI

app = FastAPI()

BOOKS = [{"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "science"},
    {"title": "Title Four", "author": "Author Four", "category": "history"},
    {"title": "Title Five", "author": "Author Five", "category": "science"},
    {"title": "Title Six", "author": "Author Two", "category": "math"}
]


@app.get('/reade books')
def first():
    return BOOKS


@app.get('/book{book_title}')
def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book




@app.get('/books/')
def read_by_category(category: str):
    book_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            book_to_return.append(book)

    return book_to_return




@app.get('/books/{auhtor}')
def read_by_author(author: str):
    book_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            book_to_return.append(book)
    return book_to_return


@app.post('/book/create_book')

def create_book(new_book):


    BOOKS.append(new_book)


@app.put('/book/updated_book')

def update_book(updated_book):
    for i in range(len(BOOKS)):
        
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book


@app.delete('/del')
def delete_book(book_title: str):
    for x in range(len(BOOKS)):
        if BOOKS[x].get('title').casefold() == book_title.casefold():
            return "BOOK DELETED"


@app.get('/books/byauthor/{author}')
def book_by_author(author: str):

    books_to_return = []

    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)

        return books_to_return