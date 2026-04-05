package com.alterix.services;

import com.alterix.models.*;
import com.alterix.builder.ExchangeBuilder;
import com.alterix.composite.*;
import com.alterix.observer.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.*;

/**
 * Core exchange service managing exchange lifecycle
 * Uses Builder, Composite, and Observer patterns
 */
public class ExchangeService {
    private static final Logger logger = LoggerFactory.getLogger(ExchangeService.class);
    
    private final Map<String, ExchangeSubject> activeExchanges;
    private final ExchangeBuilder exchangeBuilder;
    private boolean initialized;

    public ExchangeService() {
        this.activeExchanges = new HashMap<>();
        this.exchangeBuilder = new ExchangeBuilder();
        this.initialized = false;
    }

    public void initialize() {
        logger.info("Initializing ExchangeService...");
        this.initialized = true;
        logger.info("ExchangeService initialized");
    }

    public Exchange createExchange(String id, Exchange.ExchangeType type, 
                                   List<User> participants, Map<User, Skill> offerings) {
        if (!initialized) {
            throw new IllegalStateException("ExchangeService not initialized");
        }
        
        logger.info("Creating exchange: {} of type {}", id, type);
        
        // Use Builder pattern
        exchangeBuilder.reset()
            .withId(id)
            .withType(type);
        
        for (User participant : participants) {
            exchangeBuilder.addParticipant(participant);
        }
        
        for (Map.Entry<User, Skill> entry : offerings.entrySet()) {
            exchangeBuilder.addOffering(entry.getKey(), entry.getValue());
        }
        
        Exchange exchange = exchangeBuilder.build();
        
        // Create subject and attach observers
        ExchangeSubject subject = new ExchangeSubject(exchange);
        for (User participant : participants) {
            subject.attach(new UserNotificationObserver(participant));
        }
        
        activeExchanges.put(id, subject);
        subject.notifyExchangeCreated();
        
        logger.info("Exchange created successfully: {}", id);
        return exchange;
    }

    public ExchangeComponent createMultiPartyChain(String chainId, List<Exchange> exchanges) {
        logger.info("Creating multi-party exchange chain: {}", chainId);
        
        ExchangeChain chain = new ExchangeChain(chainId);
        
        for (Exchange exchange : exchanges) {
            chain.add(new ExchangeLeaf(exchange));
        }
        
        if (!chain.isValid()) {
            throw new IllegalStateException("Invalid exchange chain: not connected");
        }
        
        logger.info("Multi-party chain created with {} exchanges", exchanges.size());
        return chain;
    }

    public void updateExchangeStatus(String exchangeId, Exchange.ExchangeStatus newStatus) {
        ExchangeSubject subject = activeExchanges.get(exchangeId);
        if (subject == null) {
            throw new IllegalArgumentException("Exchange not found: " + exchangeId);
        }
        
        Exchange exchange = subject.getExchange();
        Exchange.ExchangeStatus oldStatus = exchange.getStatus();
        exchange.setStatus(newStatus);
        
        subject.notifyStatusChanged(oldStatus, newStatus);
        
        if (newStatus == Exchange.ExchangeStatus.COMPLETED) {
            subject.notifyExchangeCompleted();
        } else if (newStatus == Exchange.ExchangeStatus.CANCELLED) {
            subject.notifyExchangeCancelled();
        }
    }

    public Exchange getExchange(String exchangeId) {
        ExchangeSubject subject = activeExchanges.get(exchangeId);
        return subject != null ? subject.getExchange() : null;
    }

    public List<Exchange> getAllExchanges() {
        List<Exchange> exchanges = new ArrayList<>();
        for (ExchangeSubject subject : activeExchanges.values()) {
            exchanges.add(subject.getExchange());
        }
        return exchanges;
    }

    public void shutdown() {
        logger.info("Shutting down ExchangeService");
        activeExchanges.clear();
        this.initialized = false;
    }

    public boolean isInitialized() {
        return initialized;
    }
}
