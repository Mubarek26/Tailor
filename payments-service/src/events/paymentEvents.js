const EventEmitter = require('events');

/**
 * ============================================================================
 * DESIGN PATTERN: OBSERVER PATTERN (EVENT-DRIVEN ARCHITECTURE)
 * ============================================================================
 * Rationale: 
 * This module acts as the concrete Subject/Publisher in the Observer pattern.
 * By extending Node's native EventEmitter, it allows independent subsystems 
 * (like notification handlers, ledger loggers, and audit trails) to register 
 * themselves as Observers (listeners) to payment changes.
 * 
 * Benefits: 
 * 100% loose-coupling. The payment creation logic doesn't need to know 
 * about specific notification logic, email systems, or logging implementations.
 * ============================================================================
 */

const PAYMENT_EVENTS = {
  CREATED: 'payment.created',
  UPDATED: 'payment.updated',
};

class PaymentEventBus extends EventEmitter {}

const paymentEvents = new PaymentEventBus();

module.exports = { paymentEvents, PAYMENT_EVENTS };

