package com.alterix.chain;

import com.alterix.models.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.List;
import java.util.stream.Collectors;

/**
 * CHAIN OF RESPONSIBILITY - Concrete Handler
 * Filters users based on skill level match
 */
public class SkillLevelFilter extends MatchingHandler {
    private static final Logger logger = LoggerFactory.getLogger(SkillLevelFilter.class);

    @Override
    public List<User> handle(User requester, List<User> candidates, MatchCriteria criteria) {
        logger.info("Applying skill level filter");
        
        Skill requestedSkill = criteria.getRequestedSkill();
        if (requestedSkill == null) {
            return passToNext(requester, candidates, criteria);
        }
        
        List<User> filtered = candidates.stream()
            .filter(user -> hasMatchingSkill(user, requestedSkill))
            .collect(Collectors.toList());
        
        logger.info("Candidates after skill level filter: {}", filtered.size());
        
        return passToNext(requester, filtered, criteria);
    }

    private boolean hasMatchingSkill(User user, Skill requestedSkill) {
        return user.getOfferedSkills().stream()
            .anyMatch(skill -> 
                skill.getName().equalsIgnoreCase(requestedSkill.getName()) &&
                skill.getLevel().ordinal() >= requestedSkill.getLevel().ordinal()
            );
    }
}
