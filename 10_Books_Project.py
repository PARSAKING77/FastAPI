from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    descreption: str
    rating: int

    def __init__(self, id, title, author, descreption, rating):

        self.id = id
        self.title = title
        self.author = author
        self.descreption = descreption
        self.rating = rating

class BookRequest(BaseModel):
    id: id
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    descreption: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)

    class Config:

        schema_extra = {

            'example' : {

                'title' : 'Eneter name of your new book',
                'author' : 'Enter your name',
                'descreption' : 'Enter the Descreption of your new book',
                'rating' : 5
            }
        }


BOOKS = [

    Book(1, 'Shoe Dog', 'Folani', 'How nike makes', 8),
    Book(2, 'Roobi', 'Folan kas', 'Its about a fox goes to prison', 3),
    Book(3, 'Shafaei Zendegi', 'Giti', 'Its about soul of human', 9),
    Book(4, 'You dont know js yet', '...', 'Its about the JavaScrpict', 9)
]


@app.get('/books')
def read_all_books():
    return BOOKS




@app.post('/create-book')
def craete_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    return books.append(find_book_id(new_book))


def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1

    else:
        book.id = 1


    return book