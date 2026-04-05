package com.alterix.models;

import java.util.*;

public class User {
    private final String id;
    private String name;
    private String email;
    private List<Skill> offeredSkills;
    private List<Skill> requestedSkills;
    private TrustScore trustScore;
    private Map<String, Object> metadata;
    private boolean isActive;

    public User(String id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.offeredSkills = new ArrayList<>();
        this.requestedSkills = new ArrayList<>();
        this.trustScore = new TrustScore();
        this.metadata = new HashMap<>();
        this.isActive = true;
    }

    public String getId() { return id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    
    public List<Skill> getOfferedSkills() { return new ArrayList<>(offeredSkills); }
    public void addOfferedSkill(Skill skill) { this.offeredSkills.add(skill); }
    
    public List<Skill> getRequestedSkills() { return new ArrayList<>(requestedSkills); }
    public void addRequestedSkill(Skill skill) { this.requestedSkills.add(skill); }
    
    public TrustScore getTrustScore() { return trustScore; }
    public void setTrustScore(TrustScore trustScore) { this.trustScore = trustScore; }
    public void setTrustScore(double score) { this.trustScore = new TrustScore(); this.trustScore.updateScore(score, true); }
    
    public boolean isActive() { return isActive; }
    public void setActive(boolean active) { isActive = active; }
    
    public Map<String, Object> getMetadata() { return new HashMap<>(metadata); }
    public void setMetadata(String key, Object value) { this.metadata.put(key, value); }

    @Override
    public String toString() {
        return "User{id='" + id + "', name='" + name + "', trustScore=" + trustScore.getScore() + "}";
    }
}
