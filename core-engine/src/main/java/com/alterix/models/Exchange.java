package com.alterix.models;

import java.time.LocalDateTime;
import java.util.*;

public class Exchange {
    private final String id;
    private ExchangeType type;
    private ExchangeStatus status;
    private List<User> participants;
    private Map<User, Skill> offerings;
    private LocalDateTime createdAt;
    private LocalDateTime scheduledAt;
    private double fairnessScore;

    public enum ExchangeType {
        DIRECT_SWAP,
        PAID_LEARNING,
        MULTI_PARTY_CHAIN
    }

    public enum ExchangeStatus {
        PENDING,
        NEGOTIATING,
        SCHEDULED,
        IN_PROGRESS,
        COMPLETED,
        CANCELLED
    }

    public Exchange(String id, ExchangeType type) {
        this.id = id;
        this.type = type;
        this.status = ExchangeStatus.PENDING;
        this.participants = new ArrayList<>();
        this.offerings = new HashMap<>();
        this.createdAt = LocalDateTime.now();
        this.fairnessScore = 0.0;
    }

    public String getId() { return id; }
    public ExchangeType getType() { return type; }
    public ExchangeStatus getStatus() { return status; }
    public void setStatus(ExchangeStatus status) { this.status = status; }
    
    public List<User> getParticipants() { return new ArrayList<>(participants); }
    public void addParticipant(User user) { this.participants.add(user); }
    
    public Map<User, Skill> getOfferings() { return new HashMap<>(offerings); }
    public void addOffering(User user, Skill skill) { this.offerings.put(user, skill); }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public LocalDateTime getScheduledAt() { return scheduledAt; }
    public void setScheduledAt(LocalDateTime scheduledAt) { this.scheduledAt = scheduledAt; }
    
    public double getFairnessScore() { return fairnessScore; }
    public void setFairnessScore(double score) { this.fairnessScore = score; }

    @Override
    public String toString() {
        return "Exchange{id='" + id + "', type=" + type + ", participants=" + participants.size() + "}";
    }
}
