package com.alterix.bridge;

import com.alterix.models.*;
import java.util.List;

/**
 * BRIDGE PATTERN - Implementation Interface
 * Defines the interface for matching algorithm implementations
 */
public interface MatchingAlgorithm {
    List<User> findCandidates(User requester, List<User> allUsers);
    double calculateSimilarity(User user1, User user2);
    String getAlgorithmName();
}
