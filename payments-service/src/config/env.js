require('dotenv').config();

const env = {
  port: process.env.PAYMENTS_PORT || 5001,
  mongoUri:
    process.env.PAYMENTS_MONGO_URI ||
    process.env.MONGO_URI ||
    'mongodb://localhost:27017/tailor_shop_payments',
  coreApiBaseUrl: process.env.CORE_API_BASE_URL || 'http://localhost:5000/api',
  serviceToken: process.env.SERVICE_TOKEN || 'change-me',
  requestTimeout: Number(process.env.HTTP_TIMEOUT || 8000),
};

module.exports = { env };
