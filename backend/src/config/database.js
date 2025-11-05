const mongoose = require('mongoose');

const connectDB = async () => {
  try {
    const mongoURI = process.env.MONGODB_URI || 'mongodb://localhost:27017/lesezirkel';
    await mongoose.connect(mongoURI);
    console.log('MongoDB connected successfully');
  } catch (error) {
    console.error('MongoDB connection error:', error.message);
    console.log('Warning: Running without database connection. Data will not persist.');
    // Don't exit - allow the server to run for testing purposes
    // In production, you might want to uncomment the line below
    // process.exit(1);
  }
};

module.exports = connectDB;
