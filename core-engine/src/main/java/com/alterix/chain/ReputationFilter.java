package com.alterix.chain;

import com.alterix.models.User;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.List;
import java.util.stream.Collectors;

/**
 * CHAIN OF RESPONSIBILITY - Concrete Handler
 * Filters users based on trust score
 */
public class ReputationFilter extends MatchingHandler {
    private static final Logger logger = LoggerFactory.getLogger(ReputationFilter.class);

    @Override
    public List<User> handle(User requester, List<User> candidates, MatchCriteria criteria) {
        logger.info("Applying reputation filter. Min trust score: {}", criteria.getMinTrustScore());
        
        List<User> filtered = candidates.stream()
            .filter(user -> user.getTrustScore().getScore() >= criteria.getMinTrustScore())
            .collect(Collectors.toList());
        
        logger.info("Candidates after reputation filter: {}", filtered.size());
        
        return passToNext(requester, filtered, criteria);
    }
}
