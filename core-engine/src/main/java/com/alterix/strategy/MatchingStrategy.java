package com.alterix.strategy;

import com.alterix.models.*;
import java.util.List;

/**
 * STRATEGY PATTERN
 * Interface for different matching algorithms
 * Allows runtime selection of matching strategy
 */
public interface MatchingStrategy {
    MatchResult findMatches(User requester, List<User> candidates, Skill requestedSkill);
    String getStrategyName();
    double calculateMatchScore(User requester, User candidate, Skill requestedSkill);
}
