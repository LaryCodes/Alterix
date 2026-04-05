package com.alterix.adapter;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * ADAPTER PATTERN - Concrete Adapter
 * Adapts external payment gateway to internal payment interface
 */
public class PaymentAdapter implements ExternalServiceAdapter {
    private static final Logger logger = LoggerFactory.getLogger(PaymentAdapter.class);
    
    private boolean connected;
    private String apiKey;
    private String gatewayUrl;

    public PaymentAdapter(String apiKey, String gatewayUrl) {
        this.apiKey = apiKey;
        this.gatewayUrl = gatewayUrl;
        this.connected = false;
    }

    @Override
    public boolean connect() {
        logger.info("Connecting to payment gateway: {}", gatewayUrl);
        // Simulate connection to external payment service
        this.connected = true;
        logger.info("Payment gateway connected successfully");
        return true;
    }

    @Override
    public void disconnect() {
        logger.info("Disconnecting from payment gateway");
        this.connected = false;
    }

    @Override
    public boolean isConnected() {
        return connected;
    }

    @Override
    public String getServiceName() {
        return "PaymentGateway";
    }

    /**
     * Process payment for paid learning exchanges
     */
    public boolean processPayment(String userId, double amount, String currency) {
        if (!connected) {
            logger.error("Cannot process payment: not connected");
            return false;
        }
        
        logger.info("Processing payment: user={}, amount={} {}", userId, amount, currency);
        
        // Simulate payment processing
        boolean success = amount > 0 && amount < 10000;
        
        if (success) {
            logger.info("Payment processed successfully");
        } else {
            logger.error("Payment processing failed");
        }
        
        return success;
    }

    /**
     * Refund payment
     */
    public boolean refundPayment(String transactionId, double amount) {
        if (!connected) {
            logger.error("Cannot refund: not connected");
            return false;
        }
        
        logger.info("Processing refund: transaction={}, amount={}", transactionId, amount);
        return true;
    }

    /**
     * Get payment status
     */
    public String getPaymentStatus(String transactionId) {
        if (!connected) {
            return "DISCONNECTED";
        }
        return "COMPLETED";
    }
}
