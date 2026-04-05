package com.alterix.chain;

import com.alterix.models.Skill;

/**
 * Criteria for matching users
 */
public class MatchCriteria {
    private Skill requestedSkill;
    private double minTrustScore;
    private String location;
    private boolean requireAvailability;
    private int maxDistance;

    public MatchCriteria(Skill requestedSkill) {
        this.requestedSkill = requestedSkill;
        this.minTrustScore = 50.0;
        this.requireAvailability = true;
        this.maxDistance = 50;
    }

    public Skill getRequestedSkill() { return requestedSkill; }
    public void setRequestedSkill(Skill skill) { this.requestedSkill = skill; }
    
    public double getMinTrustScore() { return minTrustScore; }
    public void setMinTrustScore(double score) { this.minTrustScore = score; }
    
    public String getLocation() { return location; }
    public void setLocation(String location) { this.location = location; }
    
    public boolean isRequireAvailability() { return requireAvailability; }
    public void setRequireAvailability(boolean require) { this.requireAvailability = require; }
    
    public int getMaxDistance() { return maxDistance; }
    public void setMaxDistance(int distance) { this.maxDistance = distance; }
}
