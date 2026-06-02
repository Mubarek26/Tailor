const express = require('express');
const cors = require('cors');
const { errorHandler, notFound } = require('./middleware/errorHandler');
const paymentRoutes = require('./modules/payments/payments.routes');
const { setupPaymentObservers } = require('./services/notificationHandlers');

const app = express();

app.use(cors({
  origin: true,
  credentials: true,
}));
app.use(express.json());

setupPaymentObservers();

app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok' });
});

app.use('/payments', paymentRoutes);

app.use(notFound);
app.use(errorHandler);

module.exports = app;
