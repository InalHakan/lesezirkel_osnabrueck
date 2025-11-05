const mongoose = require('mongoose');

const bookSchema = new mongoose.Schema({
  title: {
    type: String,
    required: true,
    trim: true
  },
  author: {
    type: String,
    required: true,
    trim: true
  },
  isbn: {
    type: String,
    unique: true,
    sparse: true
  },
  description: {
    type: String,
    default: ''
  },
  publishedYear: {
    type: Number
  },
  status: {
    type: String,
    enum: ['available', 'reading', 'completed'],
    default: 'available'
  }
}, {
  timestamps: true
});

module.exports = mongoose.model('Book', bookSchema);
