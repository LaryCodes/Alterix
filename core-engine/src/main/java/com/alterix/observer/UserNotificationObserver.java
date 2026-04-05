package com.alterix.observer;

import com.alterix.models.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * OBSERVER PATTERN - Concrete Observer
 * Sends notifications to users about exchange events
 */
public class UserNotificationObserver implements ExchangeObserver {
    private static final Logger logger = LoggerFactory.getLogger(UserNotificationObserver.class);
    
    private final String observerId;
    private final User user;

    public UserNotificationObserver(User user) {
        this.user = user;
        this.observerId = "UserNotification_" + user.getId();
    }

    @Override
    public void onExchangeCreated(Exchange exchange) {
        logger.info("Notifying user {} of new exchange: {}", user.getId(), exchange.getId());
        sendNotification("New exchange created", 
            "You have been added to exchange: " + exchange.getId());
    }

    @Override
    public void onExchangeStatusChanged(Exchange exchange, Exchange.ExchangeStatus oldStatus, 
                                       Exchange.ExchangeStatus newStatus) {
        logger.info("Notifying user {} of status change: {} -> {}", 
            user.getId(), oldStatus, newStatus);
        sendNotification("Exchange status updated", 
            String.format("Exchange %s status changed from %s to %s", 
                exchange.getId(), oldStatus, newStatus));
    }

    @Override
    public void onExchangeCompleted(Exchange exchange) {
        logger.info("Notifying user {} of exchange completion: {}", 
            user.getId(), exchange.getId());
        sendNotification("Exchange completed", 
            "Exchange " + exchange.getId() + " has been completed successfully!");
    }

    @Override
    public void onExchangeCancelled(Exchange exchange) {
        logger.info("Notifying user {} of exchange cancellation: {}", 
            user.getId(), exchange.getId());
        sendNotification("Exchange cancelled", 
            "Exchange " + exchange.getId() + " has been cancelled");
    }

    @Override
    public String getObserverId() {
        return observerId;
    }

    private void sendNotification(String title, String message) {
        // In production, this would integrate with notification service
        logger.info("NOTIFICATION to {}: {} - {}", user.getEmail(), title, message);
    }

    public User getUser() {
        return user;
    }
}
