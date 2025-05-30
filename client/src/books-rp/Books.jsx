import React, { useEffect, useState } from 'react';
import axios from 'axios';

const API_URL = "http://localhost:8000"; // Cambia si tu backend está en otro host o puerto

const Books = () => {
  const [books, setBooks] = useState([]);
  const [newBook, setNewBook] = useState({ name: "", author: "" });

  // Obtener lista de libros al cargar
  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async () => {
    try {
      const res = await axios.get(`${API_URL}/books-list/`);
      setBooks(res.data);
    } catch (error) {
      console.error("Error al obtener libros:", error);
    }
  };

  const handleInputChange = (e) => {
    setNewBook({ ...newBook, [e.target.name]: e.target.value });
  };

  const addBook = async () => {
    try {
      const res = await axios.post(`${API_URL}/books/`, newBook);
      setBooks([...books, res.data]);
      setNewBook({ name: "", author: "" });
    } catch (error) {
      console.error("Error al agregar libro:", error);
    }
  };

  const deleteBook = async (id) => {
    try {
      await axios.delete(`${API_URL}/books-delet/${id}`);
      setBooks(books.filter(book => book.id !== id));
    } catch (error) {
      console.error("Error al eliminar libro:", error);
    }
  };

  return (
    <div>
      <h1>📚 Lista de Libros</h1>

      <input
        type="text"
        name="name"
        value={newBook.name}
        placeholder="Nombre del libro"
        onChange={handleInputChange}
      />
      <input
        type="text"
        name="author"
        value={newBook.author}
        placeholder="Autor"
        onChange={handleInputChange}
      />
      <button onClick={addBook}>Agregar Libro</button>

      <ul>
        {books.map((book) => (
          <li key={book.id}>
            <strong>{book.name}</strong> por {book.author}
            <button onClick={() => deleteBook(book.id)}>🗑 Eliminar</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Books;
