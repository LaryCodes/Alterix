package com.alterix.chain;

import com.alterix.models.*;
import java.util.List;

/**
 * CHAIN OF RESPONSIBILITY PATTERN
 * Abstract handler for processing match requests through a pipeline
 */
public abstract class MatchingHandler {
    protected MatchingHandler nextHandler;

    public void setNext(MatchingHandler handler) {
        this.nextHandler = handler;
    }

    /**
     * Process the match request and filter candidates
     * @param requester The user requesting a match
     * @param candidates List of potential matches
     * @param criteria Match criteria
     * @return Filtered list of candidates
     */
    public abstract List<User> handle(User requester, List<User> candidates, MatchCriteria criteria);

    /**
     * Pass to next handler in chain
     */
    protected List<User> passToNext(User requester, List<User> candidates, MatchCriteria criteria) {
        if (nextHandler != null) {
            return nextHandler.handle(requester, candidates, criteria);
        }
        return candidates;
    }
}
