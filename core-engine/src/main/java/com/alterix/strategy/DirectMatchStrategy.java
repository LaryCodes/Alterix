package com.alterix.strategy;

import com.alterix.models.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.*;

/**
 * STRATEGY PATTERN - Concrete Strategy
 * Direct 1:1 matching algorithm
 */
public class DirectMatchStrategy implements MatchingStrategy {
    private static final Logger logger = LoggerFactory.getLogger(DirectMatchStrategy.class);

    @Override
    public MatchResult findMatches(User requester, List<User> candidates, Skill requestedSkill) {
        logger.info("Executing direct match strategy for user: {}", requester.getId());
        
        MatchResult result = new MatchResult(UUID.randomUUID().toString(), requester);
        result.setMatchType(MatchResult.MatchType.DIRECT);
        
        for (User candidate : candidates) {
            double score = calculateMatchScore(requester, candidate, requestedSkill);
            if (score > 0.5) {
                result.addMatch(candidate, score);
            }
        }
        
        // Calculate confidence based on number of matches
        double confidence = Math.min(result.getMatches().size() * 0.2, 1.0);
        result.setConfidence(confidence);
        
        logger.info("Found {} direct matches", result.getMatches().size());
        return result;
    }

    @Override
    public double calculateMatchScore(User requester, User candidate, Skill requestedSkill) {
        double score = 0.0;
        
        // Skill match (40%)
        boolean hasSkill = candidate.getOfferedSkills().stream()
            .anyMatch(s -> s.getName().equalsIgnoreCase(requestedSkill.getName()));
        if (hasSkill) score += 0.4;
        
        // Trust score (30%)
        double trustFactor = candidate.getTrustScore().getScore() / 100.0;
        score += trustFactor * 0.3;
        
        // Reciprocal interest (30%)
        boolean reciprocalInterest = candidate.getRequestedSkills().stream()
            .anyMatch(s -> requester.getOfferedSkills().stream()
                .anyMatch(os -> os.getName().equalsIgnoreCase(s.getName())));
        if (reciprocalInterest) score += 0.3;
        
        return score;
    }

    @Override
    public String getStrategyName() {
        return "DirectMatch";
    }
}
