from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI()

# Пустий словник для збереження даних
library = {}

# Модель для книги з використанням Annotated та валідації
class Book(BaseModel):
    title: str = Field(...,
                       title="Назва книги",
                       description="Назва книги повинна бути вказана",
                       min_length=1)
    author: str = Field(...,
                        title="Автор",
                        description="Ім'я автора",
                        min_length=3,
                        max_length=50)
    pages: int = Field(...,
                       title="Кількість сторінок",
                       description="Кількість сторінок повинна бути більше 10",
                       gt=10)

# Створення нової книги
@app.post("/books/", response_model=Book)
async def create_book(book: Book):
    author = book.author
    if author not in library:
        library[author] = []
    else:
        for b in library[author]:
            if b.title.lower() == book.title.lower():
                raise HTTPException(
                    status_code=409,
                    detail=f"Книга '{book.title}' вже існує у автора {author}"
                )
    library[author].append(book)
    return book

# Отримання всіх книг автора
@app.get("/books/")
async def get_books(author: str = Query(..., title="Автор")):
    if author not in library:
        raise HTTPException(status_code=404, detail="Автор не знайдений")
    return library[author]

# Оновлення книги автора
@app.put("/books/")
async def update_book(book: Book):
    author = book.author
    if author not in library:
        raise HTTPException(status_code=404, detail="Автор не знайдений")
    for b in library[author]:
        if b.title == book.title:
            b.pages = book.pages
            return {"message": "Книга оновлена"}
    raise HTTPException(status_code=404, detail="Книга не знайдена")

# Видалення книги автора
@app.delete("/books/")
async def delete_book(title: str, author: str):
    if author not in library:
        raise HTTPException(status_code=404, detail="Автор не знайдений")
    for book in library[author]:
        if book.title == title:
            library[author].remove(book)
            return {"message": "Книга видалена"}
    raise HTTPException(status_code=404, detail="Книга не знайдена")

pip install "uvicorn[standard]"
uvicorn main: app --reload
main - main