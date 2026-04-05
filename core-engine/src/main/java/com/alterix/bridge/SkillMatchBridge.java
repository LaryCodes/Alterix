package com.alterix.bridge;

import com.alterix.models.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.*;

/**
 * BRIDGE PATTERN - Abstraction
 * Separates matching interface from algorithm implementation
 * Allows switching algorithms at runtime
 */
public class SkillMatchBridge {
    private static final Logger logger = LoggerFactory.getLogger(SkillMatchBridge.class);
    
    private MatchingAlgorithm algorithm;

    public SkillMatchBridge(MatchingAlgorithm algorithm) {
        this.algorithm = algorithm;
    }

    public void setAlgorithm(MatchingAlgorithm algorithm) {
        logger.info("Switching matching algorithm to: {}", algorithm.getAlgorithmName());
        this.algorithm = algorithm;
    }

    public List<User> findMatches(User requester, List<User> allUsers) {
        logger.info("Finding matches using algorithm: {}", algorithm.getAlgorithmName());
        return algorithm.findCandidates(requester, allUsers);
    }

    public Map<User, Double> findMatchesWithScores(User requester, List<User> allUsers) {
        List<User> candidates = algorithm.findCandidates(requester, allUsers);
        Map<User, Double> scores = new HashMap<>();
        
        for (User candidate : candidates) {
            double score = algorithm.calculateSimilarity(requester, candidate);
            scores.put(candidate, score);
        }
        
        return scores;
    }

    public String getCurrentAlgorithm() {
        return algorithm.getAlgorithmName();
    }
}
