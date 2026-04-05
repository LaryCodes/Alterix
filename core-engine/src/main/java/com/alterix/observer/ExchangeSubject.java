package com.alterix.observer;

import com.alterix.models.Exchange;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.*;

/**
 * OBSERVER PATTERN - Subject
 * Manages observers and notifies them of exchange events
 */
public class ExchangeSubject {
    private static final Logger logger = LoggerFactory.getLogger(ExchangeSubject.class);
    
    private final List<ExchangeObserver> observers;
    private final Exchange exchange;

    public ExchangeSubject(Exchange exchange) {
        this.exchange = exchange;
        this.observers = new ArrayList<>();
    }

    public void attach(ExchangeObserver observer) {
        if (!observers.contains(observer)) {
            observers.add(observer);
            logger.info("Observer {} attached to exchange {}", 
                observer.getObserverId(), exchange.getId());
        }
    }

    public void detach(ExchangeObserver observer) {
        observers.remove(observer);
        logger.info("Observer {} detached from exchange {}", 
            observer.getObserverId(), exchange.getId());
    }

    public void notifyExchangeCreated() {
        logger.info("Notifying {} observers of exchange creation", observers.size());
        for (ExchangeObserver observer : observers) {
            try {
                observer.onExchangeCreated(exchange);
            } catch (Exception e) {
                logger.error("Error notifying observer {}: {}", 
                    observer.getObserverId(), e.getMessage());
            }
        }
    }

    public void notifyStatusChanged(Exchange.ExchangeStatus oldStatus, Exchange.ExchangeStatus newStatus) {
        logger.info("Notifying {} observers of status change: {} -> {}", 
            observers.size(), oldStatus, newStatus);
        for (ExchangeObserver observer : observers) {
            try {
                observer.onExchangeStatusChanged(exchange, oldStatus, newStatus);
            } catch (Exception e) {
                logger.error("Error notifying observer {}: {}", 
                    observer.getObserverId(), e.getMessage());
            }
        }
    }

    public void notifyExchangeCompleted() {
        logger.info("Notifying {} observers of exchange completion", observers.size());
        for (ExchangeObserver observer : observers) {
            try {
                observer.onExchangeCompleted(exchange);
            } catch (Exception e) {
                logger.error("Error notifying observer {}: {}", 
                    observer.getObserverId(), e.getMessage());
            }
        }
    }

    public void notifyExchangeCancelled() {
        logger.info("Notifying {} observers of exchange cancellation", observers.size());
        for (ExchangeObserver observer : observers) {
            try {
                observer.onExchangeCancelled(exchange);
            } catch (Exception e) {
                logger.error("Error notifying observer {}: {}", 
                    observer.getObserverId(), e.getMessage());
            }
        }
    }

    public int getObserverCount() {
        return observers.size();
    }

    public Exchange getExchange() {
        return exchange;
    }
}
