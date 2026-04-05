package com.alterix.composite;

import com.alterix.models.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.*;

/**
 * COMPOSITE PATTERN - Leaf
 * Represents a single exchange (cannot have children)
 */
public class ExchangeLeaf implements ExchangeComponent {
    private static final Logger logger = LoggerFactory.getLogger(ExchangeLeaf.class);
    private final Exchange exchange;

    public ExchangeLeaf(Exchange exchange) {
        this.exchange = exchange;
    }

    @Override
    public String getId() {
        return exchange.getId();
    }

    @Override
    public void add(ExchangeComponent component) {
        throw new UnsupportedOperationException("Cannot add to a leaf exchange");
    }

    @Override
    public void remove(ExchangeComponent component) {
        throw new UnsupportedOperationException("Cannot remove from a leaf exchange");
    }

    @Override
    public ExchangeComponent getChild(int index) {
        throw new UnsupportedOperationException("Leaf has no children");
    }

    @Override
    public List<ExchangeComponent> getChildren() {
        return Collections.emptyList();
    }

    @Override
    public List<User> getAllParticipants() {
        return exchange.getParticipants();
    }

    @Override
    public double calculateTotalValue() {
        return exchange.getOfferings().values().stream()
            .mapToDouble(Skill::getValuationScore)
            .sum();
    }

    @Override
    public boolean isValid() {
        // Check if exchange has required participants and offerings
        return !exchange.getParticipants().isEmpty() 
            && !exchange.getOfferings().isEmpty()
            && exchange.getFairnessScore() >= 50.0;
    }

    @Override
    public void execute() {
        if (!isValid()) {
            throw new IllegalStateException("Cannot execute invalid exchange");
        }
        exchange.setStatus(Exchange.ExchangeStatus.IN_PROGRESS);
        logger.info("Executing exchange: {}", exchange.getId());
    }

    @Override
    public String getDescription() {
        return String.format("Exchange[%s]: %d participants, value=%.2f", 
            exchange.getId(), 
            exchange.getParticipants().size(), 
            calculateTotalValue());
    }

    public Exchange getExchange() {
        return exchange;
    }
}
