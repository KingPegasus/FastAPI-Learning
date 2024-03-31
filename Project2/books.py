'''
Move Fast with FastAPI
Pydantics - data parsing and validation
'''
from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field(gt=0)

    class Config:
        json_schema_extra = {
            'example': {
                'title': ' A book',
                'author': 'Raza',
                'description': 'A book description',
                'rating': 5,
                'published_date': 2012
            }
        }


BOOKS = [
    Book(1, 'Computer Programming', 'Raza', 'Nice', 5, 2012),
    Book(2, 'Book2', 'Author2', 'ok', 3, 2012),
    Book(3, 'Book3 Programming', 'Author3', 'Nice', 4, 2012),
    Book(4, 'Book4 Programming', 'Author4', 'Nice', 5, 2012),
    Book(5, 'Book5 Programming', 'Author5', 'poor', 1, 2012),
]


@app.get('/books', status_code=status.HTTP_200_OK)
async def read_books():
    return BOOKS


@app.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def read_books(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Book not found')


@app.get('/books/date/', status_code=status.HTTP_200_OK)
async def read_books_by_published_date(published_date: int = Query(gt=0)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


@app.get('/books/', status_code=status.HTTP_200_OK)
async def read_books(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.post('/create-book', status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    # Note: ** means "treat the key-value pairs in the dictionary as additional named arguments to this function call."
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id+1
    else:
        book.id = 1
    return book


@app.put('/books/update_book', status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Book not found')


@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='Book not found')
