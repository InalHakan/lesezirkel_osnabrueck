import React from 'react';

function SessionList({ sessions, onEdit, onDelete }) {
  if (sessions.length === 0) {
    return (
      <div style={{ 
        padding: '40px', 
        textAlign: 'center', 
        backgroundColor: '#f8f9fa',
        borderRadius: '8px'
      }}>
        <p style={{ fontSize: '18px', color: '#6c757d' }}>
          Keine Lesetermine gefunden. Erstellen Sie einen neuen Termin!
        </p>
      </div>
    );
  }

  return (
    <div style={{ display: 'grid', gap: '20px' }}>
      {sessions.map((session) => (
        <div 
          key={session._id}
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
              <h3 style={{ margin: '0 0 10px 0', color: '#333' }}>
                {session.bookId?.title || 'Buch gelöscht'}
              </h3>
              <p style={{ margin: '5px 0', color: '#666' }}>
                <strong>Datum:</strong> {new Date(session.date).toLocaleDateString('de-DE')}
              </p>
              <p style={{ margin: '5px 0', color: '#666' }}>
                <strong>Ort:</strong> {session.location}
              </p>
              {session.participants && session.participants.length > 0 && (
                <p style={{ margin: '5px 0', color: '#666' }}>
                  <strong>Teilnehmer:</strong> {session.participants.join(', ')}
                </p>
              )}
              {session.notes && (
                <p style={{ margin: '10px 0', color: '#555', fontStyle: 'italic' }}>
                  {session.notes}
                </p>
              )}
            </div>
            <div style={{ display: 'flex', gap: '10px', marginLeft: '20px' }}>
              <button
                onClick={() => onEdit(session)}
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
                onClick={() => onDelete(session._id)}
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

export default SessionList;
