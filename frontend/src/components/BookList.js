import React from 'react';

function BookList({ books, onEdit, onDelete }) {
  if (books.length === 0) {
    return (
      <div style={{ 
        padding: '40px', 
        textAlign: 'center', 
        backgroundColor: '#f8f9fa',
        borderRadius: '8px'
      }}>
        <p style={{ fontSize: '18px', color: '#6c757d' }}>
          Keine Bücher gefunden. Fügen Sie Ihr erstes Buch hinzu!
        </p>
      </div>
    );
  }

  return (
    <div style={{ display: 'grid', gap: '20px' }}>
      {books.map((book) => (
        <div 
          key={book._id}
          style={{
            border: '1px solid #dee2e6',
            borderRadius: '8px',
            padding: '20px',
            backgroundColor: 'white',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
            <div style={{ flex: 1 }}>
              <h3 style={{ margin: '0 0 10px 0', color: '#333' }}>{book.title}</h3>
              <p style={{ margin: '5px 0', color: '#666' }}>
                <strong>Autor:</strong> {book.author}
              </p>
              {book.isbn && (
                <p style={{ margin: '5px 0', color: '#666' }}>
                  <strong>ISBN:</strong> {book.isbn}
                </p>
              )}
              {book.publishedYear && (
                <p style={{ margin: '5px 0', color: '#666' }}>
                  <strong>Jahr:</strong> {book.publishedYear}
                </p>
              )}
              {book.description && (
                <p style={{ margin: '10px 0', color: '#555' }}>
                  {book.description}
                </p>
              )}
              <p style={{ margin: '10px 0' }}>
                <span style={{
                  display: 'inline-block',
                  padding: '4px 12px',
                  borderRadius: '12px',
                  fontSize: '14px',
                  backgroundColor: book.status === 'completed' ? '#d4edda' :
                                    book.status === 'reading' ? '#fff3cd' : '#d1ecf1',
                  color: book.status === 'completed' ? '#155724' :
                         book.status === 'reading' ? '#856404' : '#0c5460'
                }}>
                  {book.status === 'completed' ? 'Abgeschlossen' :
                   book.status === 'reading' ? 'Lesen' : 'Verfügbar'}
                </span>
              </p>
            </div>
            <div style={{ display: 'flex', gap: '10px', marginLeft: '20px' }}>
              <button
                onClick={() => onEdit(book)}
                style={{
                  padding: '8px 16px',
                  backgroundColor: '#ffc107',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                Bearbeiten
              </button>
              <button
                onClick={() => onDelete(book._id)}
                style={{
                  padding: '8px 16px',
                  backgroundColor: '#dc3545',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                Löschen
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default BookList;
