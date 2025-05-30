from fastapi import FastAPI, HTTPException, status, Body
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from typing import List, Optional
import httpx
from pydantic import BaseModel, Field

from config.db import book_collection, cedulas_collection, rucs_collection  # Importa colecciones desde db.py

# --- Modelos Pydantic ---

class Book(BaseModel):
    name: str
    author: str

class BookOut(Book):
    id: str = Field(..., alias="_id")

class BookUpdate(BaseModel):
    name: Optional[str] = None
    author: Optional[str] = None

class NumeroIdentificacion(BaseModel):
    numero: str

# --- FastAPI app ---

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def serialize_book(book) -> dict:
    return {
        "id": str(book["_id"]),
        "name": book["name"],
        "author": book["author"],
    }

# --- Funciones para validar cédula y RUC ---

async def validar_cedula(cedula: str) -> bool:
    url = "https://srienlinea.sri.gob.ec/sri-registro-civil-servicio-internet/rest/DatosRegistroCivil/existeNumeroIdentificacion"
    params = {"numeroIdentificacion": cedula}
    headers = {"User-Agent": "Mozilla/5.0"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json() is True
        else:
            raise HTTPException(status_code=response.status_code, detail="Error al consultar cédula")

async def validar_ruc(ruc: str) -> bool:
    url = "https://srienlinea.sri.gob.ec/sri-catastro-sujeto-servicio-internet/rest/ConsolidadoContribuyente/existePorNumeroRuc"
    params = {"numeroRuc": ruc}
    headers = {"User-Agent": "Mozilla/5.0"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json() is True
        else:
            raise HTTPException(status_code=response.status_code, detail="Error al consultar RUC")

# --- Endpoints para validar cédula y RUC (POST) ---

@app.post("/validar/cedula")
async def validar_cedula_post(data: NumeroIdentificacion):
    existe = await validar_cedula(data.numero)
    if existe:
        cedulas_collection.insert_one({"numero": data.numero})
    return {"cedula": data.numero, "existe": existe}

@app.post("/validar/ruc")
async def validar_ruc_post(data: NumeroIdentificacion):
    existe = await validar_ruc(data.numero)
    if existe:
        rucs_collection.insert_one({"numero": data.numero})
    return {"ruc": data.numero, "existe": existe}

# --- Endpoints para eliminar cédula y RUC (POST) ---

@app.post("/delete/cedula")
def delete_cedula(data: NumeroIdentificacion = Body(...)):
    result = cedulas_collection.delete_one({"numero": data.numero})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Cédula no encontrada para eliminar")
    return {"message": f"Cédula {data.numero} eliminada correctamente"}

@app.post("/delete/ruc")
def delete_ruc(data: NumeroIdentificacion = Body(...)):
    result = rucs_collection.delete_one({"numero": data.numero})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="RUC no encontrado para eliminar")
    return {"message": f"RUC {data.numero} eliminado correctamente"}

# --- Endpoints CRUD libros ---

@app.post("/books/", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(book: Book = Body(...)):
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
