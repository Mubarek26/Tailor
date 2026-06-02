const AppError = require('../utils/appError');
const { env } = require('../config/env');

const serviceAuth = (req, res, next) => {
  const token = req.headers['x-service-token'];

  if (!env.serviceToken || env.serviceToken === 'change-me') {
    return next(new AppError('Service token is not configured', 500));
  }

  if (token !== env.serviceToken) {
    return next(new AppError('Unauthorized service request', 401));
  }

  return next();
};

module.exports = { serviceAuth };
