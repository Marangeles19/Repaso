from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from typing import List

from models.models import Book, BookOut, BookUpdate
from config.db import book_collection

app = FastAPI()

# Configurar CORS para permitir solicitudes desde React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Aquí va la URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serializador de libros
def serialize_book(book) -> dict:
    return {
        "id": str(book["_id"]),
        "name": book["name"],
        "author": book["author"]
    }

@app.post("/books/", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(book: Book):
    print(f"📥 Recibido en POST /books/: {book.dict()}")
    result = book_collection.insert_one(book.dict())
    new_book = book_collection.find_one({"_id": result.inserted_id})
    return serialize_book(new_book)

@app.get("/books-list/", response_model=List[BookOut])
def get_books():
    books = book_collection.find()
    return [serialize_book(book) for book in books]

@app.get("/books-forID/{book_id}", response_model=BookOut)
def get_book(book_id: str):
    try:
        obj_id = ObjectId(book_id)
    except:
        raise HTTPException(status_code=400, detail="ID inválido")

    book = book_collection.find_one({"_id": obj_id})
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return serialize_book(book)

@app.put("/books-update/{book_id}", response_model=BookOut)
def update_book(book_id: str, book_update: BookUpdate):
    try:
        obj_id = ObjectId(book_id)
    except:
        raise HTTPException(status_code=400, detail="ID inválido")

    update_data = book_update.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No hay datos para actualizar")

    result = book_collection.update_one({"_id": obj_id}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Libro no encontrado o datos iguales")

    updated_book = book_collection.find_one({"_id": obj_id})
    return serialize_book(updated_book)

@app.delete("/books-delet/{book_id}")
def delete_book(book_id: str):
    try:
        obj_id = ObjectId(book_id)
    except:
        raise HTTPException(status_code=400, detail="ID inválido")

    result = book_collection.delete_one({"_id": obj_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    return {"message": f"Libro {book_id} eliminado correctamente"}

