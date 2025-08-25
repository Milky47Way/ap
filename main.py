from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI()

library = {}

class Book(BaseModel):
    title: str = Field(..., title="Назва книги", description="Назва книги повинна бути вказана", min_length=1)
    author: str = Field(..., title="Автор", description="Ім'я автора", min_length=3, max_length=50)
    pages: str = Field(..., title="Кількість сторінок", description="К-сть більше 10", gt=10)

@app.post("/books/", response_model=Book):
async def create_book(book: Book):
    author = book.author
    if author not in library:
        library[author] = []
    else:
        for b in library[author]:
            if b.title.lower() == book.title.lower():
                raise HTTPException(status_code=409, detail=f"Книга'{book.title}' вже існує у автора {author}")

            library[author].append