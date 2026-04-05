package com.alterix.chain;

import com.alterix.models.User;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.List;
import java.util.stream.Collectors;

/**
 * CHAIN OF RESPONSIBILITY - Concrete Handler
 * Filters users based on availability
 */
public class AvailabilityFilter extends MatchingHandler {
    private static final Logger logger = LoggerFactory.getLogger(AvailabilityFilter.class);

    @Override
    public List<User> handle(User requester, List<User> candidates, MatchCriteria criteria) {
        logger.info("Applying availability filter. Candidates before: {}", candidates.size());
        
        List<User> filtered = candidates.stream()
            .filter(User::isActive)
            .collect(Collectors.toList());
        
        logger.info("Candidates after availability filter: {}", filtered.size());
        
        return passToNext(requester, filtered, criteria);
    }
}
