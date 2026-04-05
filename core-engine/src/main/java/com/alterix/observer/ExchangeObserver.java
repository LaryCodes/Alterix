package com.alterix.observer;

import com.alterix.models.Exchange;

/**
 * OBSERVER PATTERN
 * Interface for objects that want to be notified of exchange events
 */
public interface ExchangeObserver {
    void onExchangeCreated(Exchange exchange);
    void onExchangeStatusChanged(Exchange exchange, Exchange.ExchangeStatus oldStatus, Exchange.ExchangeStatus newStatus);
    void onExchangeCompleted(Exchange exchange);
    void onExchangeCancelled(Exchange exchange);
    String getObserverId();
}
