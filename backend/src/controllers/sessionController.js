const ReadingSession = require('../models/ReadingSession');

// Get all reading sessions
exports.getAllSessions = async (req, res) => {
  try {
    const sessions = await ReadingSession.find()
      .populate('bookId')
      .sort({ date: -1 });
    res.json(sessions);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// Get a single reading session
exports.getSessionById = async (req, res) => {
  try {
    const session = await ReadingSession.findById(req.params.id).populate('bookId');
    if (!session) {
      return res.status(404).json({ message: 'Reading session not found' });
    }
    res.json(session);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// Create a new reading session
exports.createSession = async (req, res) => {
  const session = new ReadingSession({
    bookId: req.body.bookId,
    date: req.body.date,
    location: req.body.location,
    participants: req.body.participants,
    notes: req.body.notes
  });

  try {
    const newSession = await session.save();
    res.status(201).json(newSession);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
};

// Update a reading session
exports.updateSession = async (req, res) => {
  try {
    const session = await ReadingSession.findById(req.params.id);
    if (!session) {
      return res.status(404).json({ message: 'Reading session not found' });
    }

    Object.keys(req.body).forEach(key => {
      session[key] = req.body[key];
    });

    const updatedSession = await session.save();
    res.json(updatedSession);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
};

// Delete a reading session
exports.deleteSession = async (req, res) => {
  try {
    const session = await ReadingSession.findById(req.params.id);
    if (!session) {
      return res.status(404).json({ message: 'Reading session not found' });
    }

    await session.deleteOne();
    res.json({ message: 'Reading session deleted successfully' });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};
