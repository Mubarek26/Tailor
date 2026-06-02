const { asyncHandler } = require('../../utils/asyncHandler');
const AppError = require('../../utils/appError');
const Payment = require('./payments.model');
const { paymentStrategyFactory } = require('../../services/paymentStrategies');
const orderClient = require('../../services/orderClient');
const { paymentEvents, PAYMENT_EVENTS } = require('../../events/paymentEvents');

const getPopulatedOrder = (order) => ({
  _id: order._id,
  total_price: order.total_price,
  deposit: order.deposit,
  remaining_price: order.remaining_price,
  appointment_date: order.appointment_date,
  status: order.status,
});

const computeBalanceFromHistory = (total, history) => {
  const hasFull = history.some((entry) => entry.payment_type === 'full');
  if (hasFull) {
    return { deposit: Number(total || 0), remaining_price: 0 };
  }

  const deposit = history.reduce((sum, entry) => sum + Number(entry.amount || 0), 0);
  return { deposit, remaining_price: Math.max(0, Number(total || 0) - deposit) };
};

const getPayment = asyncHandler(async (req, res, next) => {
  const orderId = req.params.orderId;
  if (!orderId) return next(new AppError('orderId is required', 400));

  const paymentDoc = await Payment.findOne({ order_id: orderId });
  const payments = paymentDoc ? paymentDoc.history : [];

  payments.sort((a, b) => new Date(b.payment_date) - new Date(a.payment_date));

  return res.status(200).json({ status: 'success', results: payments.length, data: { payments } });
});

const createPayment = asyncHandler(async (req, res, next) => {
  const { order_id, amount, payment_type, payment_date } = req.body;
  if (!order_id || amount == null || !payment_type) {
    return next(new AppError('order_id, amount and payment_type are required', 400));
  }

  const order = await orderClient.getOrderBalance(order_id);
  if (!order) return next(new AppError('Order not found', 404));

  let paymentDoc = await Payment.findOne({ order_id });
  if (!paymentDoc) {
    paymentDoc = new Payment({ order_id, history: [] });
  }

  const newHistoryItem = {
    amount: Number(amount),
    payment_type,
    payment_date: payment_date || new Date(),
  };

  paymentDoc.history.push(newHistoryItem);
  await paymentDoc.save();

  const strategy = paymentStrategyFactory(payment_type);
  const nextBalance = strategy.compute({
    total: order.total_price,
    currentDeposit: order.deposit,
    amount: Number(amount),
  });

  const updatedOrder = await orderClient.updateOrderBalance(order_id, nextBalance);

  const paymentObj = paymentDoc.history[paymentDoc.history.length - 1].toObject();
  paymentObj.order_id = getPopulatedOrder(updatedOrder);

  paymentEvents.emit(PAYMENT_EVENTS.CREATED, {
    orderId: order_id,
    paymentId: paymentObj._id,
    amount: paymentObj.amount,
    payment_type: paymentObj.payment_type,
  });

  res.status(201).json({ status: 'success', data: { payment: paymentObj } });
});

const updatePayment = asyncHandler(async (req, res, next) => {
  const id = req.params.id;
  if (!id) return next(new AppError('Payment id is required', 400));

  const paymentDoc = await Payment.findOne({ 'history._id': id });
  if (!paymentDoc) return next(new AppError('Payment not found', 404));

  const historyItem = paymentDoc.history.id(id);
  const { amount, payment_type, payment_date } = req.body;

  if (amount != null) historyItem.amount = Number(amount);
  if (payment_type) historyItem.payment_type = payment_type;
  if (payment_date) historyItem.payment_date = payment_date;

  await paymentDoc.save();

  const order = await orderClient.getOrderBalance(paymentDoc.order_id);
  if (!order) return next(new AppError('Related order not found', 404));

  const nextBalance = computeBalanceFromHistory(order.total_price, paymentDoc.history);
  const updatedOrder = await orderClient.updateOrderBalance(paymentDoc.order_id, nextBalance);

  const paymentObj = historyItem.toObject();
  paymentObj.order_id = getPopulatedOrder(updatedOrder);

  paymentEvents.emit(PAYMENT_EVENTS.UPDATED, {
    orderId: paymentDoc.order_id,
    paymentId: paymentObj._id,
  });

  res.status(200).json({ status: 'success', data: { payment: paymentObj } });
});

module.exports = { getPayment, createPayment, updatePayment };
