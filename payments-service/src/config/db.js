const mongoose = require('mongoose');
const { env } = require('./env');

/**
 * ============================================================================
 * DESIGN PATTERN: SINGLETON PATTERN
 * ============================================================================
 * Rationale: 
 * Establishing connections to external datastores (like MongoDB) is highly 
 * resource-heavy and computationally expensive.
 * 
 * This module implements a Singleton by caching the connection promise (`connectionPromise`). 
 * Subsequent requests to connect to the database do not instantiate new connections, 
 * but instead reuse the existing, globally cached connection pool.
 * ============================================================================
 */
let connectionPromise = null;

const connectDb = async () => {
  if (!connectionPromise) {
    mongoose.set('strictQuery', true);
    connectionPromise = mongoose.connect(env.mongoUri).then(() => {
      console.log('Payments service connected to MongoDB');
      return mongoose.connection;
    });
  }

  return connectionPromise;
};

module.exports = { connectDb };

