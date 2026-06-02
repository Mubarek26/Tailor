const { paymentEvents, PAYMENT_EVENTS } = require('../events/paymentEvents');

const setupPaymentObservers = () => {
  paymentEvents.on(PAYMENT_EVENTS.CREATED, (payload) => {
    console.log(`[Payments] Created payment for order ${payload.orderId}`);
  });

  paymentEvents.on(PAYMENT_EVENTS.UPDATED, (payload) => {
    console.log(`[Payments] Updated payment ${payload.paymentId} for order ${payload.orderId}`);
  });
};

module.exports = { setupPaymentObservers };
