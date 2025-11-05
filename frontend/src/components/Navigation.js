import React from 'react';
import { Link, useLocation } from 'react-router-dom';

function Navigation() {
  const location = useLocation();

  const navStyle = {
    backgroundColor: '#343a40',
    padding: '15px 20px',
    marginBottom: '20px'
  };

  const navContainerStyle = {
    maxWidth: '1200px',
    margin: '0 auto',
    display: 'flex',
    alignItems: 'center',
    gap: '30px'
  };

  const linkStyle = {
    color: 'white',
    textDecoration: 'none',
    fontSize: '16px',
    padding: '8px 16px',
    borderRadius: '4px',
    transition: 'background-color 0.3s'
  };

  const activeLinkStyle = {
    ...linkStyle,
    backgroundColor: '#495057'
  };

  const titleStyle = {
    color: 'white',
    margin: 0,
    fontSize: '20px',
    marginRight: 'auto'
  };

  return (
    <nav style={navStyle}>
      <div style={navContainerStyle}>
        <h1 style={titleStyle}>Lesezirkel Osnabrück</h1>
        <Link 
          to="/" 
          style={location.pathname === '/' ? activeLinkStyle : linkStyle}
        >
          Home
        </Link>
        <Link 
          to="/books" 
          style={location.pathname === '/books' ? activeLinkStyle : linkStyle}
        >
          Bücher
        </Link>
        <Link 
          to="/sessions" 
          style={location.pathname === '/sessions' ? activeLinkStyle : linkStyle}
        >
          Lesetermine
        </Link>
      </div>
    </nav>
  );
}

export default Navigation;
