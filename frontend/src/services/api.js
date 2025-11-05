import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const bookService = {
  getAllBooks: () => api.get('/books'),
  getBookById: (id) => api.get(`/books/${id}`),
  createBook: (book) => api.post('/books', book),
  updateBook: (id, book) => api.put(`/books/${id}`, book),
  deleteBook: (id) => api.delete(`/books/${id}`),
};

export const sessionService = {
  getAllSessions: () => api.get('/sessions'),
  getSessionById: (id) => api.get(`/sessions/${id}`),
  createSession: (session) => api.post('/sessions', session),
  updateSession: (id, session) => api.put(`/sessions/${id}`, session),
  deleteSession: (id) => api.delete(`/sessions/${id}`),
};

export default api;
