const express = require('express');
const { getPayment, createPayment, updatePayment } = require('./payments.controller');
const { serviceAuth } = require('../../middleware/serviceAuth');

const router = express.Router();

router.use(serviceAuth);

router.get('/:orderId', getPayment);
router.post('/', createPayment);
router.put('/:id', updatePayment);

module.exports = router;
