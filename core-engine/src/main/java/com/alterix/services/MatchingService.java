package com.alterix.services;

import com.alterix.models.*;
import com.alterix.strategy.*;
import com.alterix.chain.*;
import com.alterix.bridge.*;
import com.alterix.bridge.implementations.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.*;

/**
 * Core matching service that orchestrates the matching process
 * Uses Strategy, Chain of Responsibility, and Bridge patterns
 */
public class MatchingService {
    private static final Logger logger = LoggerFactory.getLogger(MatchingService.class);
    
    private MatchingStrategy currentStrategy;
    private MatchingHandler filterChain;
    private SkillMatchBridge matchBridge;
    private boolean initialized;

    public MatchingService() {
        this.initialized = false;
    }

    public void initialize() {
        logger.info("Initializing MatchingService...");
        
        // Set default strategy
        this.currentStrategy = new DirectMatchStrategy();
        
        // Build filter chain
        buildFilterChain();
        
        // Initialize bridge with default algorithm
        this.matchBridge = new SkillMatchBridge(new CollaborativeFilteringAlgorithm());
        
        this.initialized = true;
        logger.info("MatchingService initialized");
    }

    private void buildFilterChain() {
        MatchingHandler availability = new AvailabilityFilter();
        MatchingHandler reputation = new ReputationFilter();
        MatchingHandler skillLevel = new SkillLevelFilter();
        
        availability.setNext(reputation);
        reputation.setNext(skillLevel);
        
        this.filterChain = availability;
    }

    public MatchResult findMatches(User requester, List<User> allUsers, Skill requestedSkill) {
        if (!initialized) {
            throw new IllegalStateException("MatchingService not initialized");
        }
        
        logger.info("Finding matches for user: {}", requester.getId());
        
        // Apply filter chain
        MatchCriteria criteria = new MatchCriteria(requestedSkill);
        List<User> filteredCandidates = filterChain.handle(requester, allUsers, criteria);
        
        // Apply matching strategy
        MatchResult result = currentStrategy.findMatches(requester, filteredCandidates, requestedSkill);
        
        logger.info("Found {} matches for user {}", result.getMatches().size(), requester.getId());
        return result;
    }

    public void setStrategy(MatchingStrategy strategy) {
        logger.info("Changing matching strategy to: {}", strategy.getStrategyName());
        this.currentStrategy = strategy;
    }

    public void setMatchingAlgorithm(MatchingAlgorithm algorithm) {
        matchBridge.setAlgorithm(algorithm);
    }

    public void shutdown() {
        logger.info("Shutting down MatchingService");
        this.initialized = false;
    }

    public boolean isInitialized() {
        return initialized;
    }
}
