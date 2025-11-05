import React, { useState, useEffect } from 'react';
import { bookService } from '../services/api';
import BookList from '../components/BookList';
import BookForm from '../components/BookForm';

function BooksPage() {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingBook, setEditingBook] = useState(null);

  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async () => {
    try {
      setLoading(true);
      const response = await bookService.getAllBooks();
      setBooks(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch books. Please check if the backend is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddBook = () => {
    setEditingBook(null);
    setShowForm(true);
  };

  const handleEditBook = (book) => {
    setEditingBook(book);
    setShowForm(true);
  };

  const handleDeleteBook = async (id) => {
    if (window.confirm('Möchten Sie dieses Buch wirklich löschen?')) {
      try {
        await bookService.deleteBook(id);
        fetchBooks();
      } catch (err) {
        alert('Fehler beim Löschen des Buchs');
        console.error(err);
      }
    }
  };

  const handleFormSubmit = async (bookData) => {
    try {
      if (editingBook) {
        await bookService.updateBook(editingBook._id, bookData);
      } else {
        await bookService.createBook(bookData);
      }
      setShowForm(false);
      setEditingBook(null);
      fetchBooks();
    } catch (err) {
      alert('Fehler beim Speichern des Buchs');
      console.error(err);
    }
  };

  const handleFormCancel = () => {
    setShowForm(false);
    setEditingBook(null);
  };

  if (loading) {
    return <div style={{ padding: '20px' }}>Loading books...</div>;
  }

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>Bücher</h1>
        <button 
          onClick={handleAddBook}
          style={{
            padding: '10px 20px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Neues Buch hinzufügen
        </button>
      </div>

      {error && (
        <div style={{ 
          padding: '10px', 
          backgroundColor: '#f8d7da', 
          color: '#721c24', 
          borderRadius: '4px',
          marginBottom: '20px'
        }}>
          {error}
        </div>
      )}

      {showForm && (
        <BookForm
          book={editingBook}
          onSubmit={handleFormSubmit}
          onCancel={handleFormCancel}
        />
      )}

      <BookList
        books={books}
        onEdit={handleEditBook}
        onDelete={handleDeleteBook}
      />
    </div>
  );
}

export default BooksPage;
