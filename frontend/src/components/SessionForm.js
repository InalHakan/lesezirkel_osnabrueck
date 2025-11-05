import React, { useState } from 'react';

function SessionForm({ session, books, onSubmit, onCancel }) {
  const [formData, setFormData] = useState({
    bookId: session?.bookId?._id || session?.bookId || '',
    date: session?.date ? new Date(session.date).toISOString().split('T')[0] : '',
    location: session?.location || 'Osnabrück',
    participants: session?.participants?.join(', ') || '',
    notes: session?.notes || ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const dataToSubmit = {
      ...formData,
      participants: formData.participants
        ? formData.participants.split(',').map(p => p.trim()).filter(p => p)
        : []
    };
    onSubmit(dataToSubmit);
  };

  return (
    <div style={{
      border: '1px solid #dee2e6',
      borderRadius: '8px',
      padding: '20px',
      marginBottom: '20px',
      backgroundColor: 'white'
    }}>
      <h2 style={{ marginTop: 0 }}>
        {session ? 'Lesetermin bearbeiten' : 'Neuer Lesetermin'}
      </h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
            Buch *
          </label>
          <select
            name="bookId"
            value={formData.bookId}
            onChange={handleChange}
            required
            style={{
              width: '100%',
              padding: '8px',
              borderRadius: '4px',
              border: '1px solid #ced4da'
            }}
          >
            <option value="">Buch auswählen...</option>
            {books.map(book => (
              <option key={book._id} value={book._id}>
                {book.title} - {book.author}
              </option>
            ))}
          </select>
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
            Datum *
          </label>
          <input
            type="date"
            name="date"
            value={formData.date}
            onChange={handleChange}
            required
            style={{
              width: '100%',
              padding: '8px',
              borderRadius: '4px',
              border: '1px solid #ced4da'
            }}
          />
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
            Ort
          </label>
          <input
            type="text"
            name="location"
            value={formData.location}
            onChange={handleChange}
            style={{
              width: '100%',
              padding: '8px',
              borderRadius: '4px',
              border: '1px solid #ced4da'
            }}
          />
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
            Teilnehmer (durch Komma getrennt)
          </label>
          <input
            type="text"
            name="participants"
            value={formData.participants}
            onChange={handleChange}
            placeholder="z.B. Anna, Max, Sophie"
            style={{
              width: '100%',
              padding: '8px',
              borderRadius: '4px',
              border: '1px solid #ced4da'
            }}
          />
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
            Notizen
          </label>
          <textarea
            name="notes"
            value={formData.notes}
            onChange={handleChange}
            rows="4"
            style={{
              width: '100%',
              padding: '8px',
              borderRadius: '4px',
              border: '1px solid #ced4da',
              fontFamily: 'inherit'
            }}
          />
        </div>

        <div style={{ display: 'flex', gap: '10px' }}>
          <button
            type="submit"
            style={{
              padding: '10px 20px',
              backgroundColor: '#28a745',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Speichern
          </button>
          <button
            type="button"
            onClick={onCancel}
            style={{
              padding: '10px 20px',
              backgroundColor: '#6c757d',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Abbrechen
          </button>
        </div>
      </form>
    </div>
  );
}

export default SessionForm;
