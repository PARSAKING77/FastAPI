from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status
app = FastAPI()


class Book:
    def __init__(self, id: int, title: str, author: str, description: str, rating: int, publish_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.publish_date = publish_date


class BookRequest(BaseModel):
    id: int
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)  
    rating: int = Field(gt=0, lt=6)
    publish_date : int



BOOKS = [
    Book(1, 'Shoe Dog', 'Folani', 'How Nike makes', 8, 2024),
    Book(2, 'Roobi', 'Folan kas', 'It\'s about a fox that goes to prison', 3, 2019),
    Book(3, 'Shafaei Zendegi', 'Giti', 'It\'s about the soul of a human', 9, 2023),
    Book(4, 'You Don\'t Know JS Yet', '...', 'It\'s about JavaScript', 9, 2009)
]



@app.get('/books', status_code=status.HTTP_200_OK)
def read_all_books():
    return BOOKS



@app.get('/books/{book_id}')
def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:

        if book.id == book_id:
            return book
            
    raise HTTPException(status_code=404, detail='Item NOT FOUND')


@app.get('/books/')
def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []

    for books in BOOKS:
        if book.rating == book_rating:

            books_to_return.append(book)

        return books_to_return

@app.get('/book/publish')
def read_books_by_publish_date(published_date: int):
    books_to_return = []

    for book in BOOKS:
        if book.publish_date == published_date:
            books_to_return.append(book)
    return books_to_return




@app.post('/create-book')
def create_book(book_request: BookRequest, status_code=status.HTTP_201_CREATED):
    new_book = Book(**book_request.dict())

    find_book_id(new_book)
    BOOKS.append(new_book)  



def find_book_id(book: Book = Path(gt=0)):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book


@app.put('/books/update_book')
def update_book(book: BookRequest):
    book_change = False

    for x in range(len(BOOKS)):

        if BOOKS[x].id == book.id:
            BOOKS[x] = book
    if not book_change:
        raise HTTPException(status_code=404, detail='Item Not FOUND')

@app.delete('/books/{book_id}')
def delete_book(book_id: int = Path(gt=0)):

    for x in range(len(BOOKS)):

        if BOOKS[x].id == book_id:

            BOOKS.pop(x)

            break