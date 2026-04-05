package com.alterix.services;

import com.alterix.models.Skill;
import com.alterix.command.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.*;

/**
 * Service for managing skill valuations
 * Uses Command pattern for undo/redo capability
 */
public class ValuationService {
    private static final Logger logger = LoggerFactory.getLogger(ValuationService.class);
    
    private final CommandInvoker commandInvoker;
    private final Map<String, Double> marketRates;
    private boolean initialized;

    public ValuationService() {
        this.commandInvoker = new CommandInvoker();
        this.marketRates = new HashMap<>();
        this.initialized = false;
    }

    public void initialize() {
        logger.info("Initializing ValuationService...");
        initializeMarketRates();
        this.initialized = true;
        logger.info("ValuationService initialized");
    }

    private void initializeMarketRates() {
        marketRates.put("Technology", 1.5);
        marketRates.put("Business", 1.4);
        marketRates.put("Creative", 1.3);
        marketRates.put("Language", 1.2);
        marketRates.put("Other", 1.0);
    }

    public void updateValuation(Skill skill, double newValue) {
        if (!initialized) {
            throw new IllegalStateException("ValuationService not initialized");
        }
        
        ValuationCommand command = new ValuationCommand(skill, newValue);
        commandInvoker.executeCommand(command);
    }

    public double calculateValuation(Skill skill) {
        double baseValue = skill.getValuationScore();
        double categoryMultiplier = marketRates.getOrDefault(skill.getCategory(), 1.0);
        double levelMultiplier = getLevelMultiplier(skill.getLevel());
        
        return baseValue * categoryMultiplier * levelMultiplier;
    }

    private double getLevelMultiplier(Skill.SkillLevel level) {
        return switch (level) {
            case BEGINNER -> 1.0;
            case INTERMEDIATE -> 1.5;
            case ADVANCED -> 2.0;
            case EXPERT -> 3.0;
        };
    }

    public void undoLastValuation() {
        commandInvoker.undo();
    }

    public void redoLastValuation() {
        commandInvoker.redo();
    }

    public List<String> getValuationHistory() {
        return commandInvoker.getCommandHistory();
    }

    public void shutdown() {
        logger.info("Shutting down ValuationService");
        commandInvoker.clearHistory();
        this.initialized = false;
    }

    public boolean isInitialized() {
        return initialized;
    }
}
