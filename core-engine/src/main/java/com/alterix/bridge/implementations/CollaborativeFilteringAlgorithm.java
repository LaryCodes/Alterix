package com.alterix.bridge.implementations;

import com.alterix.bridge.MatchingAlgorithm;
import com.alterix.models.*;
import java.util.*;
import java.util.stream.Collectors;

/**
 * BRIDGE PATTERN - Concrete Implementation
 * Collaborative filtering based matching algorithm
 */
public class CollaborativeFilteringAlgorithm implements MatchingAlgorithm {

    @Override
    public List<User> findCandidates(User requester, List<User> allUsers) {
        return allUsers.stream()
            .filter(u -> !u.equals(requester))
            .filter(u -> calculateSimilarity(requester, u) > 0.3)
            .sorted((u1, u2) -> Double.compare(
                calculateSimilarity(requester, u2),
                calculateSimilarity(requester, u1)
            ))
            .limit(10)
            .collect(Collectors.toList());
    }

    @Override
    public double calculateSimilarity(User user1, User user2) {
        Set<String> skills1 = user1.getOfferedSkills().stream()
            .map(Skill::getName)
            .collect(Collectors.toSet());
        
        Set<String> skills2 = user2.getOfferedSkills().stream()
            .map(Skill::getName)
            .collect(Collectors.toSet());
        
        Set<String> intersection = new HashSet<>(skills1);
        intersection.retainAll(skills2);
        
        Set<String> union = new HashSet<>(skills1);
        union.addAll(skills2);
        
        return union.isEmpty() ? 0.0 : (double) intersection.size() / union.size();
    }

    @Override
    public String getAlgorithmName() {
        return "CollaborativeFiltering";
    }
}
