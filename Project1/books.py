'''
FastAPI Request Method Logic
'''
from fastapi import FastAPI, Body


app = FastAPI()


BOOKS = [
    {"title": "t1", "category": "science", "Author": "A1"},
    {"title": "t2", "category": "math", "Author": "A2"},
    {"title": "t3", "category": "science", "Author": "A3"},
    {"title": "t4", "category": "math", "Author": "A4"},
    {"title": "t5", "category": "science", "Author": "A5"}
]


@app.get("/")
async def first_api():
    return {'message': 'first'}


@app.get("/books")
async def books():
    return BOOKS


@app.get("/books/{book_title}")
async def read_books(book_title):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
    return "Not Found"


@app.get("/books/")
async def read_books_by_catergory(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


@app.get("/books/{book_author}/")
async def read_author_books_by_catergory(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('Author').casefold() == book_author.casefold() and \
                book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


@app.get("/books/author/{book_author}")
async def read_books_by_author(book_author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('Author').casefold() == book_author.casefold():
            books_to_return.append(book)
    return books_to_return


@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book


@app.delete("/books/delete_book/{book_title}")
async def update_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
