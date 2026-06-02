const axios = require('axios');
const { env } = require('../config/env');
const AppError = require('../utils/appError');

/**
 * ============================================================================
 * DESIGN PATTERN: ADAPTER PATTERN
 * ============================================================================
 * Rationale: 
 * Adapts and normalizes the external Core API's HTTP endpoints and raw response 
 * formats into a clean, local programmatic interface that the rest of the 
 * payments service relies on.
 * 
 * It handles the conversion of network payloads, status checks, and provides
 * a unified JavaScript interface (`getOrderBalance`, `updateOrderBalance`) 
 * representing target operations.
 * ============================================================================
 */

const client = axios.create({
  baseURL: env.coreApiBaseUrl,
  timeout: env.requestTimeout,
});

const serviceHeaders = () => ({
  'x-service-token': env.serviceToken,
});

const parseOrder = (payload) => {
  if (!payload) return null;
  if (payload.data?.order) return payload.data.order;
  if (payload.order) return payload.order;
  if (payload.data) return payload.data;
  return payload;
};

const getOrderBalance = async (orderId) => {
  try {
    const res = await client.get(`/orders/${orderId}/balance`, {
      headers: serviceHeaders(),
    });
    return parseOrder(res.data);
  } catch (error) {
    throw new AppError('Failed to fetch order balance', 502);
  }
};

const updateOrderBalance = async (orderId, balance) => {
  try {
    const res = await client.patch(`/orders/${orderId}/balance`, balance, {
      headers: serviceHeaders(),
    });
    return parseOrder(res.data);
  } catch (error) {
    throw new AppError('Failed to update order balance', 502);
  }
};

module.exports = { getOrderBalance, updateOrderBalance };

