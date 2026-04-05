package com.alterix.core;

import com.alterix.services.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * SINGLETON PATTERN
 * Ensures single instance of the core system engine.
 * Thread-safe implementation using Bill Pugh Singleton Design.
 */
public class SystemCore {
    private static final Logger logger = LoggerFactory.getLogger(SystemCore.class);
    
    private final MatchingService matchingService;
    private final ExchangeService exchangeService;
    private final ValuationService valuationService;
    private final TrustService trustService;
    private boolean initialized;

    private SystemCore() {
        logger.info("Initializing Alterix Core Engine...");
        this.matchingService = new MatchingService();
        this.exchangeService = new ExchangeService();
        this.valuationService = new ValuationService();
        this.trustService = new TrustService();
        this.initialized = false;
    }

    /**
     * Bill Pugh Singleton - Thread-safe without synchronization overhead
     */
    private static class SingletonHelper {
        private static final SystemCore INSTANCE = new SystemCore();
    }

    public static SystemCore getInstance() {
        return SingletonHelper.INSTANCE;
    }

    public synchronized void initialize() {
        if (!initialized) {
            logger.info("Starting system initialization...");
            matchingService.initialize();
            exchangeService.initialize();
            valuationService.initialize();
            trustService.initialize();
            initialized = true;
            logger.info("System initialization complete");
        }
    }

    public synchronized void shutdown() {
        if (initialized) {
            logger.info("Shutting down system...");
            matchingService.shutdown();
            exchangeService.shutdown();
            valuationService.shutdown();
            trustService.shutdown();
            initialized = false;
            logger.info("System shutdown complete");
        }
    }

    public MatchingService getMatchingService() { return matchingService; }
    public ExchangeService getExchangeService() { return exchangeService; }
    public ValuationService getValuationService() { return valuationService; }
    public TrustService getTrustService() { return trustService; }
    public boolean isInitialized() { return initialized; }

    // Prevent cloning
    @Override
    protected Object clone() throws CloneNotSupportedException {
        throw new CloneNotSupportedException("Cannot clone singleton instance");
    }
}
