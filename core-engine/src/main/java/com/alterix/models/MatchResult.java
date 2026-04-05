package com.alterix.models;

import java.util.*;

public class MatchResult {
    private final String id;
    private User requester;
    private List<User> matches;
    private Map<User, Double> matchScores;
    private List<List<User>> multiHopPaths;
    private MatchType matchType;
    private double confidence;

    public enum MatchType {
        DIRECT,
        MULTI_HOP,
        HYBRID
    }

    public MatchResult(String id, User requester) {
        this.id = id;
        this.requester = requester;
        this.matches = new ArrayList<>();
        this.matchScores = new HashMap<>();
        this.multiHopPaths = new ArrayList<>();
        this.matchType = MatchType.DIRECT;
        this.confidence = 0.0;
    }

    public String getId() { return id; }
    public User getRequester() { return requester; }
    
    public List<User> getMatches() { return new ArrayList<>(matches); }
    public void addMatch(User user, double score) {
        this.matches.add(user);
        this.matchScores.put(user, score);
    }
    
    public Map<User, Double> getMatchScores() { return new HashMap<>(matchScores); }
    
    public List<List<User>> getMultiHopPaths() { return new ArrayList<>(multiHopPaths); }
    public void addMultiHopPath(List<User> path) { this.multiHopPaths.add(new ArrayList<>(path)); }
    
    public MatchType getMatchType() { return matchType; }
    public void setMatchType(MatchType type) { this.matchType = type; }
    
    public double getConfidence() { return confidence; }
    public void setConfidence(double confidence) { this.confidence = confidence; }

    public User getBestMatch() {
        return matches.stream()
            .max(Comparator.comparing(matchScores::get))
            .orElse(null);
    }
}
