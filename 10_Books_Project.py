from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    def __init__(self, id: int, title: str, author: str, description: str, rating: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating



class BookRequest(BaseModel):
    id: int
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)  # Corrected spelling
    rating: int = Field(gt=0, lt=6)




BOOKS = [
    Book(1, 'Shoe Dog', 'Folani', 'How Nike makes', 8),
    Book(2, 'Roobi', 'Folan kas', 'It\'s about a fox that goes to prison', 3),
    Book(3, 'Shafaei Zendegi', 'Giti', 'It\'s about the soul of a human', 9),
    Book(4, 'You Don\'t Know JS Yet', '...', 'It\'s about JavaScript', 9)
]



@app.get('/books')
def read_all_books():
    return BOOKS



@app.post('/create-book')
def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())

    find_book_id(new_book)
    BOOKS.append(new_book)  

    return new_book



def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book



@app.get('/books/{book_id}')

def read_book(book_id: int):
    for book in BOOKS:

        if book.id == book_id:
            return book
            
    return {"error": "Book not found"}