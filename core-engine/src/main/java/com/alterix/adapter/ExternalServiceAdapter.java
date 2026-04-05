package com.alterix.adapter;

/**
 * ADAPTER PATTERN
 * Interface for adapting external services to internal system
 */
public interface ExternalServiceAdapter {
    boolean connect();
    void disconnect();
    boolean isConnected();
    String getServiceName();
}
