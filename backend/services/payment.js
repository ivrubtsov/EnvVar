const stripe = require('stripe')(process.env.STRIPE_API_KEY);
const crypto = require('crypto');

class PaymentService {
  constructor() {
    this.stripeWebhookSecret = process.env.STRIPE_WEBHOOK_SECRET;
    this.currency = process.env.DEFAULT_CURRENCY || 'usd';
  }

  async createPaymentIntent(amount, customerId) {
    return await stripe.paymentIntents.create({
      amount,
      currency: this.currency,
      customer: customerId,
      metadata: {
        environment: process.env.NODE_ENV
      }
    });
  }

  verifyWebhook(payload, signature) {
    return stripe.webhooks.constructEvent(
      payload,
      signature,
      this.stripeWebhookSecret
    );
  }

  async processRefund(chargeId) {
    const refundReason = process.env.REFUND_REASON || 'requested_by_customer';
    return await stripe.refunds.create({
      charge: chargeId,
      reason: refundReason
    });
  }
}

module.exports = PaymentService;
