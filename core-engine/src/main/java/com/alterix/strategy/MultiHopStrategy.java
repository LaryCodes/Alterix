package com.alterix.strategy;

import com.alterix.models.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.*;

/**
 * STRATEGY PATTERN - Concrete Strategy
 * Multi-hop matching algorithm (A → B → C)
 * Finds indirect exchange paths
 */
public class MultiHopStrategy implements MatchingStrategy {
    private static final Logger logger = LoggerFactory.getLogger(MultiHopStrategy.class);
    private static final int MAX_HOP_DEPTH = 4;

    @Override
    public MatchResult findMatches(User requester, List<User> candidates, Skill requestedSkill) {
        logger.info("Executing multi-hop strategy for user: {}", requester.getId());
        
        MatchResult result = new MatchResult(UUID.randomUUID().toString(), requester);
        result.setMatchType(MatchResult.MatchType.MULTI_HOP);
        
        // Build graph of potential connections
        Map<User, List<User>> graph = buildConnectionGraph(candidates);
        
        // Find paths from requester to users with requested skill
        List<User> targetUsers = findUsersWithSkill(candidates, requestedSkill);
        
        for (User target : targetUsers) {
            List<List<User>> paths = findPaths(requester, target, graph, MAX_HOP_DEPTH);
            for (List<User> path : paths) {
                result.addMultiHopPath(path);
                double score = calculatePathScore(path);
                result.addMatch(target, score);
            }
        }
        
        double confidence = result.getMultiHopPaths().isEmpty() ? 0.0 : 0.8;
        result.setConfidence(confidence);
        
        logger.info("Found {} multi-hop paths", result.getMultiHopPaths().size());
        return result;
    }

    private Map<User, List<User>> buildConnectionGraph(List<User> users) {
        Map<User, List<User>> graph = new HashMap<>();
        
        for (User user : users) {
            List<User> connections = new ArrayList<>();
            for (User other : users) {
                if (!user.equals(other) && hasConnection(user, other)) {
                    connections.add(other);
                }
            }
            graph.put(user, connections);
        }
        
        return graph;
    }

    private boolean hasConnection(User user1, User user2) {
        // Users are connected if one offers what the other requests
        return user1.getOfferedSkills().stream()
            .anyMatch(offered -> user2.getRequestedSkills().stream()
                .anyMatch(requested -> offered.getName().equalsIgnoreCase(requested.getName())));
    }

    private List<User> findUsersWithSkill(List<User> users, Skill skill) {
        List<User> result = new ArrayList<>();
        for (User user : users) {
            if (user.getOfferedSkills().stream()
                .anyMatch(s -> s.getName().equalsIgnoreCase(skill.getName()))) {
                result.add(user);
            }
        }
        return result;
    }

    private List<List<User>> findPaths(User start, User end, Map<User, List<User>> graph, int maxDepth) {
        List<List<User>> allPaths = new ArrayList<>();
        List<User> currentPath = new ArrayList<>();
        Set<User> visited = new HashSet<>();
        
        currentPath.add(start);
        visited.add(start);
        
        dfs(start, end, graph, currentPath, visited, allPaths, maxDepth);
        
        return allPaths;
    }

    private void dfs(User current, User target, Map<User, List<User>> graph, 
                     List<User> path, Set<User> visited, List<List<User>> allPaths, int depth) {
        if (depth <= 0) return;
        
        if (current.equals(target)) {
            allPaths.add(new ArrayList<>(path));
            return;
        }
        
        List<User> neighbors = graph.getOrDefault(current, Collections.emptyList());
        for (User neighbor : neighbors) {
            if (!visited.contains(neighbor)) {
                visited.add(neighbor);
                path.add(neighbor);
                
                dfs(neighbor, target, graph, path, visited, allPaths, depth - 1);
                
                path.remove(path.size() - 1);
                visited.remove(neighbor);
            }
        }
    }

    private double calculatePathScore(List<User> path) {
        if (path.isEmpty()) return 0.0;
        
        // Shorter paths are better
        double lengthPenalty = 1.0 / path.size();
        
        // Average trust score of path
        double avgTrust = path.stream()
            .mapToDouble(u -> u.getTrustScore().getScore())
            .average()
            .orElse(0.0) / 100.0;
        
        return (lengthPenalty * 0.4) + (avgTrust * 0.6);
    }

    @Override
    public double calculateMatchScore(User requester, User candidate, Skill requestedSkill) {
        // For multi-hop, score is based on path quality
        return 0.7; // Default score for multi-hop matches
    }

    @Override
    public String getStrategyName() {
        return "MultiHop";
    }
}
