from fastapi import FastAPI, Body


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


books = [

    Book(1, 'Shoe Dog', 'Folani', 'How nike makes', 8),
    Book(2, 'Roobi', 'Folan kas', 'Its about a fox goes to prison', 3),
    Book(3, 'Shafaei Zendegi', 'Giti', 'Its about soul of human', 9),
    Book(4, 'You dont know js yet', '...', 'Its about the JavaScrpict', 9)
]


@app.get('/books')
def read_all_books():
    return books




@app.post('/create-book')
def craete_book(book_request=Body()):
    return books.append(book_request)