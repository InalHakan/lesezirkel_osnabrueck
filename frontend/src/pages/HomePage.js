import React from 'react';

function HomePage() {
  return (
    <div style={{ padding: '40px', maxWidth: '800px', margin: '0 auto' }}>
      <h1 style={{ color: '#333', marginBottom: '20px' }}>Willkommen beim Lesezirkel Osnabrück</h1>
      
      <div style={{ 
        backgroundColor: '#f8f9fa', 
        padding: '30px', 
        borderRadius: '8px',
        marginBottom: '30px'
      }}>
        <p style={{ fontSize: '18px', lineHeight: '1.6', marginBottom: '15px' }}>
          Unser Lesezirkel ist eine Gemeinschaft von Bücherliebhabern, die sich regelmäßig treffen, 
          um über Literatur zu diskutieren und neue Bücher zu entdecken.
        </p>
        <p style={{ fontSize: '16px', lineHeight: '1.6' }}>
          Nutzen Sie diese Anwendung, um:
        </p>
        <ul style={{ fontSize: '16px', lineHeight: '1.8' }}>
          <li>Unsere Bücherliste zu durchsuchen und zu verwalten</li>
          <li>Lesetermine zu planen und zu organisieren</li>
          <li>Notizen zu Diskussionen festzuhalten</li>
        </ul>
      </div>

      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: '1fr 1fr', 
        gap: '20px',
        marginTop: '30px'
      }}>
        <div style={{
          padding: '20px',
          backgroundColor: '#e7f3ff',
          borderRadius: '8px',
          textAlign: 'center'
        }}>
          <h3 style={{ marginBottom: '10px' }}>📚 Bücher</h3>
          <p>Verwalten Sie die Bücherliste des Lesezirkels</p>
        </div>
        <div style={{
          padding: '20px',
          backgroundColor: '#fff3cd',
          borderRadius: '8px',
          textAlign: 'center'
        }}>
          <h3 style={{ marginBottom: '10px' }}>📅 Lesetermine</h3>
          <p>Organisieren Sie Treffen und Diskussionen</p>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
