import React, { useState, useEffect } from 'react';
import { sessionService, bookService } from '../services/api';
import SessionList from '../components/SessionList';
import SessionForm from '../components/SessionForm';

function SessionsPage() {
  const [sessions, setSessions] = useState([]);
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingSession, setEditingSession] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [sessionsResponse, booksResponse] = await Promise.all([
        sessionService.getAllSessions(),
        bookService.getAllBooks()
      ]);
      setSessions(sessionsResponse.data);
      setBooks(booksResponse.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch data. Please check if the backend is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddSession = () => {
    setEditingSession(null);
    setShowForm(true);
  };

  const handleEditSession = (session) => {
    setEditingSession(session);
    setShowForm(true);
  };

  const handleDeleteSession = async (id) => {
    if (window.confirm('Are you sure you want to delete this reading session?')) {
      try {
        await sessionService.deleteSession(id);
        fetchData();
      } catch (err) {
        alert('Failed to delete session');
        console.error(err);
      }
    }
  };

  const handleFormSubmit = async (sessionData) => {
    try {
      if (editingSession) {
        await sessionService.updateSession(editingSession._id, sessionData);
      } else {
        await sessionService.createSession(sessionData);
      }
      setShowForm(false);
      setEditingSession(null);
      fetchData();
    } catch (err) {
      alert('Failed to save session');
      console.error(err);
    }
  };

  const handleFormCancel = () => {
    setShowForm(false);
    setEditingSession(null);
  };

  if (loading) {
    return <div style={{ padding: '20px' }}>Loading sessions...</div>;
  }

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>Lesetermine</h1>
        <button 
          onClick={handleAddSession}
          style={{
            padding: '10px 20px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Neuer Lesetermin
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
        <SessionForm
          session={editingSession}
          books={books}
          onSubmit={handleFormSubmit}
          onCancel={handleFormCancel}
        />
      )}

      <SessionList
        sessions={sessions}
        onEdit={handleEditSession}
        onDelete={handleDeleteSession}
      />
    </div>
  );
}

export default SessionsPage;
