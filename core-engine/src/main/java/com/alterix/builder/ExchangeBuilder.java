package com.alterix.builder;

import com.alterix.models.*;
import java.time.LocalDateTime;
import java.util.*;

/**
 * BUILDER PATTERN
 * Constructs complex Exchange objects step-by-step with validation
 */
public class ExchangeBuilder {
    private String id;
    private Exchange.ExchangeType type;
    private List<User> participants;
    private Map<User, Skill> offerings;
    private LocalDateTime scheduledAt;
    private double fairnessScore;

    public ExchangeBuilder() {
        this.participants = new ArrayList<>();
        this.offerings = new HashMap<>();
        this.fairnessScore = 0.0;
    }

    public ExchangeBuilder withId(String id) {
        this.id = id;
        return this;
    }

    public ExchangeBuilder withType(Exchange.ExchangeType type) {
        this.type = type;
        return this;
    }

    public ExchangeBuilder addParticipant(User user) {
        if (user == null) {
            throw new IllegalArgumentException("Participant cannot be null");
        }
        this.participants.add(user);
        return this;
    }

    public ExchangeBuilder addOffering(User user, Skill skill) {
        if (user == null || skill == null) {
            throw new IllegalArgumentException("User and skill cannot be null");
        }
        if (!participants.contains(user)) {
            throw new IllegalStateException("User must be added as participant first");
        }
        this.offerings.put(user, skill);
        return this;
    }

    public ExchangeBuilder scheduleAt(LocalDateTime dateTime) {
        if (dateTime.isBefore(LocalDateTime.now())) {
            throw new IllegalArgumentException("Cannot schedule in the past");
        }
        this.scheduledAt = dateTime;
        return this;
    }

    public ExchangeBuilder withFairnessScore(double score) {
        if (score < 0 || score > 100) {
            throw new IllegalArgumentException("Fairness score must be between 0 and 100");
        }
        this.fairnessScore = score;
        return this;
    }

    /**
     * Validates and builds the Exchange object
     */
    public Exchange build() {
        validate();
        
        Exchange exchange = new Exchange(id, type);
        
        for (User participant : participants) {
            exchange.addParticipant(participant);
        }
        
        for (Map.Entry<User, Skill> entry : offerings.entrySet()) {
            exchange.addOffering(entry.getKey(), entry.getValue());
        }
        
        if (scheduledAt != null) {
            exchange.setScheduledAt(scheduledAt);
        }
        
        exchange.setFairnessScore(fairnessScore);
        
        return exchange;
    }

    private void validate() {
        if (id == null || id.isEmpty()) {
            throw new IllegalStateException("Exchange ID is required");
        }
        if (type == null) {
            throw new IllegalStateException("Exchange type is required");
        }
        if (participants.isEmpty()) {
            throw new IllegalStateException("At least one participant is required");
        }
        if (offerings.isEmpty()) {
            throw new IllegalStateException("At least one offering is required");
        }
        
        // Type-specific validation
        switch (type) {
            case DIRECT_SWAP:
                if (participants.size() != 2) {
                    throw new IllegalStateException("Direct swap requires exactly 2 participants");
                }
                if (offerings.size() != 2) {
                    throw new IllegalStateException("Direct swap requires 2 offerings");
                }
                break;
            case MULTI_PARTY_CHAIN:
                if (participants.size() < 3) {
                    throw new IllegalStateException("Multi-party chain requires at least 3 participants");
                }
                break;
        }
    }

    /**
     * Reset builder for reuse
     */
    public ExchangeBuilder reset() {
        this.id = null;
        this.type = null;
        this.participants.clear();
        this.offerings.clear();
        this.scheduledAt = null;
        this.fairnessScore = 0.0;
        return this;
    }
}
