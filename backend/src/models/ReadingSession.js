const mongoose = require('mongoose');

const readingSessionSchema = new mongoose.Schema({
  bookId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Book',
    required: true
  },
  date: {
    type: Date,
    required: true
  },
  location: {
    type: String,
    default: 'Osnabrück'
  },
  participants: [{
    type: String
  }],
  notes: {
    type: String,
    default: ''
  }
}, {
  timestamps: true
});

module.exports = mongoose.model('ReadingSession', readingSessionSchema);
