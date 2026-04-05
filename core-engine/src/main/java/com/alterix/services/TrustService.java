package com.alterix.services;

import com.alterix.models.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.*;

/**
 * Service for managing trust scores and reputation
 */
public class TrustService {
    private static final Logger logger = LoggerFactory.getLogger(TrustService.class);
    
    private final Map<String, List<TrustEdge>> trustGraph;
    private boolean initialized;

    private static class TrustEdge {
        User from;
        User to;
        double weight;
        
        TrustEdge(User from, User to, double weight) {
            this.from = from;
            this.to = to;
            this.weight = weight;
        }
    }

    public TrustService() {
        this.trustGraph = new HashMap<>();
        this.initialized = false;
    }

    public void initialize() {
        logger.info("Initializing TrustService...");
        this.initialized = true;
        logger.info("TrustService initialized");
    }

    public void updateTrustScore(User user, double rating, boolean successful) {
        if (!initialized) {
            throw new IllegalStateException("TrustService not initialized");
        }
        
        user.getTrustScore().updateScore(rating, successful);
        logger.info("Updated trust score for user {}: {}", 
            user.getId(), user.getTrustScore().getScore());
    }

    public void addTrustConnection(User from, User to, double weight) {
        String key = from.getId();
        trustGraph.computeIfAbsent(key, k -> new ArrayList<>())
            .add(new TrustEdge(from, to, weight));
        
        logger.info("Added trust connection: {} -> {} (weight: {})", 
            from.getId(), to.getId(), weight);
    }

    public double calculateTrustPath(User from, User to) {
        // Simple BFS to find trust path
        Queue<User> queue = new LinkedList<>();
        Map<String, Double> trustScores = new HashMap<>();
        Set<String> visited = new HashSet<>();
        
        queue.offer(from);
        trustScores.put(from.getId(), 1.0);
        visited.add(from.getId());
        
        while (!queue.isEmpty()) {
            User current = queue.poll();
            
            if (current.equals(to)) {
                return trustScores.get(to.getId());
            }
            
            List<TrustEdge> edges = trustGraph.getOrDefault(current.getId(), Collections.emptyList());
            for (TrustEdge edge : edges) {
                if (!visited.contains(edge.to.getId())) {
                    double newScore = trustScores.get(current.getId()) * edge.weight;
                    trustScores.put(edge.to.getId(), newScore);
                    visited.add(edge.to.getId());
                    queue.offer(edge.to);
                }
            }
        }
        
        return 0.0; // No path found
    }

    public Map<String, Object> getTrustAnalytics(User user) {
        Map<String, Object> analytics = new HashMap<>();
        TrustScore score = user.getTrustScore();
        
        analytics.put("score", score.getScore());
        analytics.put("totalExchanges", score.getTotalExchanges());
        analytics.put("successfulExchanges", score.getSuccessfulExchanges());
        analytics.put("averageRating", score.getAverageRating());
        analytics.put("reportCount", score.getReportCount());
        analytics.put("successRate", 
            score.getTotalExchanges() > 0 
                ? (double) score.getSuccessfulExchanges() / score.getTotalExchanges() 
                : 0.0);
        
        return analytics;
    }

    public void shutdown() {
        logger.info("Shutting down TrustService");
        trustGraph.clear();
        this.initialized = false;
    }

    public boolean isInitialized() {
        return initialized;
    }
}
