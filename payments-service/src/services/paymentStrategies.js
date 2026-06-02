const AppError = require('../utils/appError');

/**
 * ============================================================================
 * DESIGN PATTERN: STRATEGY PATTERN (OO ABSTRACTION)
 * ============================================================================
 * Rationale:
 * Calculates deposit and remaining balances dynamically based on the payment type selected.
 * Instead of writing complex, hard-to-maintain nested conditionals inside the payments controller,
 * each mathematical algorithm is encapsulated in a dedicated strategy class conforming to 
 * the abstract 'PaymentStrategy' interface.
 * 
 * Benefits:
 * High extensibility. If we decide to add support for installment payments, partial refunds,
 * or discount promotions, we can simply create a new strategy class inheriting from 
 * PaymentStrategy without altering any existing payment controller or order updates code.
 * ============================================================================
 */

// Abstract Strategy Base Class (OO Abstraction Principle)
class PaymentStrategy {
  constructor() {
    if (this.constructor === PaymentStrategy) {
      throw new Error("Cannot instantiate abstract class PaymentStrategy directly.");
    }
  }

  compute({ total, currentDeposit, amount }) {
    throw new Error("Method 'compute()' must be implemented by concrete subclasses.");
  }
}

// Concrete Strategy A: Computes intermediate balance updates (deposits)
class DepositStrategy extends PaymentStrategy {
  compute({ total, currentDeposit, amount }) {
    const nextDeposit = Number(currentDeposit || 0) + Number(amount || 0);
    return {
      deposit: nextDeposit,
      remaining_price: Math.max(0, Number(total || 0) - nextDeposit),
    };
  }
}

// Concrete Strategy B: Computes final closing balance updates (full payoff)
class FullPaymentStrategy extends PaymentStrategy {
  compute({ total }) {
    return {
      deposit: Number(total || 0),
      remaining_price: 0,
    };
  }
}

/**
 * ============================================================================
 * DESIGN PATTERN: SIMPLE FACTORY PATTERN
 * ============================================================================
 * Rationale:
 * Decouples the client (the payments controller) from concrete strategy instantiation.
 * The calling controller does not need to know which class to instantiate; it simply passes 
 * a string identifier (`paymentType`), and the Factory returns the appropriate strategy object.
 * ============================================================================
 */
const paymentStrategyFactory = (paymentType) => {
  if (paymentType === 'deposit') return new DepositStrategy();
  if (paymentType === 'full') return new FullPaymentStrategy();
  throw new AppError('Invalid payment_type', 400);
};

module.exports = { paymentStrategyFactory };

