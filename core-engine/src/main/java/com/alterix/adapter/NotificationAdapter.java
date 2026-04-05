package com.alterix.adapter;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.*;

/**
 * ADAPTER PATTERN - Concrete Adapter
 * Adapts external notification services (email, SMS, push) to internal interface
 */
public class NotificationAdapter implements ExternalServiceAdapter {
    private static final Logger logger = LoggerFactory.getLogger(NotificationAdapter.class);
    
    private boolean connected;
    private String serviceEndpoint;
    private Map<String, String> config;

    public NotificationAdapter(String serviceEndpoint) {
        this.serviceEndpoint = serviceEndpoint;
        this.config = new HashMap<>();
        this.connected = false;
    }

    @Override
    public boolean connect() {
        logger.info("Connecting to notification service: {}", serviceEndpoint);
        this.connected = true;
        logger.info("Notification service connected");
        return true;
    }

    @Override
    public void disconnect() {
        logger.info("Disconnecting from notification service");
        this.connected = false;
    }

    @Override
    public boolean isConnected() {
        return connected;
    }

    @Override
    public String getServiceName() {
        return "NotificationService";
    }

    /**
     * Send email notification
     */
    public boolean sendEmail(String to, String subject, String body) {
        if (!connected) {
            logger.error("Cannot send email: not connected");
            return false;
        }
        
        logger.info("Sending email to {}: {}", to, subject);
        return true;
    }

    /**
     * Send push notification
     */
    public boolean sendPushNotification(String userId, String title, String message) {
        if (!connected) {
            logger.error("Cannot send push notification: not connected");
            return false;
        }
        
        logger.info("Sending push notification to {}: {}", userId, title);
        return true;
    }

    /**
     * Send SMS
     */
    public boolean sendSMS(String phoneNumber, String message) {
        if (!connected) {
            logger.error("Cannot send SMS: not connected");
            return false;
        }
        
        logger.info("Sending SMS to {}", phoneNumber);
        return true;
    }

    public void setConfig(String key, String value) {
        config.put(key, value);
    }
}
