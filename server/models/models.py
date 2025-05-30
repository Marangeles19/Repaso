
from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    name: str
    author: str

class BookOut(Book):
    id: str

class BookUpdate(BaseModel):
    name: Optional[str] = None
    author: Optional[str] = None
