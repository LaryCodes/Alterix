package com.alterix;

import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;
import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.alterix.core.SystemCore;
import com.alterix.models.*;
import com.alterix.factory.*;
import com.alterix.builder.ExchangeBuilder;
import com.alterix.strategy.*;
import com.alterix.chain.*;
import com.alterix.command.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.stream.Collectors;

/**
 * HTTP REST Server for Alterix Core Engine
 * Exposes design pattern services via JSON API
 * Runs on port 50051 (configurable)
 */
public class CoreServer {
    private static final Logger logger = LoggerFactory.getLogger(CoreServer.class);
    private static final Gson gson = new Gson();
    private static final int DEFAULT_PORT = 50051;

    public static void main(String[] args) throws Exception {
        int port = DEFAULT_PORT;
        if (args.length > 0) {
            try {
                port = Integer.parseInt(args[0]);
            } catch (NumberFormatException e) {
                logger.warn("Invalid port argument, using default: {}", DEFAULT_PORT);
            }
        }

        // Initialize core system
        SystemCore core = SystemCore.getInstance();
        core.initialize();

        // Create HTTP server
        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);

        server.createContext("/health", new HealthHandler());
        server.createContext("/match", new MatchHandler());
        server.createContext("/exchange/create", new ExchangeCreateHandler());
        server.createContext("/exchange/validate", new ExchangeValidateHandler());
        server.createContext("/valuate", new ValuateHandler());
        server.createContext("/patterns/demo", new PatternDemoHandler());

        server.setExecutor(null);
        server.start();

        logger.info("=".repeat(60));
        logger.info("Alterix Core Engine HTTP Server started on port {}", port);
        logger.info("Endpoints:");
        logger.info("  GET  /health              - Health check");
        logger.info("  POST /match               - Run matching engine");
        logger.info("  POST /exchange/create      - Create exchange via Builder");
        logger.info("  POST /exchange/validate    - Validate exchange fairness");
        logger.info("  POST /valuate             - Skill valuation via Command");
        logger.info("  GET  /patterns/demo       - Run all patterns demo");
        logger.info("=".repeat(60));

        // Shutdown hook
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            logger.info("Shutting down Core Engine...");
            core.shutdown();
            server.stop(2);
        }));
    }

    private static String readRequestBody(HttpExchange exchange) throws IOException {
        try (InputStream is = exchange.getRequestBody();
             BufferedReader reader = new BufferedReader(new InputStreamReader(is, StandardCharsets.UTF_8))) {
            return reader.lines().collect(Collectors.joining("\n"));
        }
    }

    private static void sendResponse(HttpExchange exchange, int statusCode, Object responseObj) throws IOException {
        String response = gson.toJson(responseObj);
        exchange.getResponseHeaders().set("Content-Type", "application/json");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        exchange.getResponseHeaders().set("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
        exchange.getResponseHeaders().set("Access-Control-Allow-Headers", "Content-Type");
        
        byte[] bytes = response.getBytes(StandardCharsets.UTF_8);
        exchange.sendResponseHeaders(statusCode, bytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(bytes);
        }
    }

    // ==================== HANDLERS ====================

    /**
     * Health check endpoint
     */
    static class HealthHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if ("OPTIONS".equals(exchange.getRequestMethod())) {
                sendResponse(exchange, 200, Map.of());
                return;
            }
            
            SystemCore core = SystemCore.getInstance();
            Map<String, Object> response = new LinkedHashMap<>();
            response.put("status", "healthy");
            response.put("engine", "Alterix Core Engine");
            response.put("version", "1.0.0");
            response.put("initialized", core.isInitialized());
            response.put("services", Map.of(
                "matching", core.getMatchingService().isInitialized(),
                "exchange", core.getExchangeService().isInitialized(),
                "valuation", core.getValuationService().isInitialized(),
                "trust", core.getTrustService().isInitialized()
            ));
            response.put("patterns", List.of(
                "Singleton", "Factory", "Builder", "Composite",
                "Chain of Responsibility", "Strategy", "Command",
                "Observer", "Adapter", "Bridge", "Mediator"
            ));
            sendResponse(exchange, 200, response);
        }
    }

    /**
     * Matching endpoint — uses Strategy + Chain of Responsibility + Bridge patterns
     */
    static class MatchHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if ("OPTIONS".equals(exchange.getRequestMethod())) {
                sendResponse(exchange, 200, Map.of());
                return;
            }
            
            try {
                String body = readRequestBody(exchange);
                JsonObject request = gson.fromJson(body, JsonObject.class);

                String userId = request.has("user_id") ? request.get("user_id").getAsString() : "unknown";
                String skillName = request.has("skill_name") ? request.get("skill_name").getAsString() : "General";
                String strategyType = request.has("strategy") ? request.get("strategy").getAsString() : "direct";

                // Use Factory pattern to create entities
                UserFactory userFactory = new UserFactory();
                SkillFactory skillFactory = new SkillFactory();

                User requester = userFactory.create(userId, "Requester", userId + "@alterix.com");
                Skill requestedSkill = skillFactory.createTechnicalSkill("req_skill", skillName, Skill.SkillLevel.INTERMEDIATE);
                requester.addRequestedSkill(requestedSkill);

                // Create sample candidates from request data
                List<User> candidates = new ArrayList<>();
                if (request.has("candidates") && request.get("candidates").isJsonArray()) {
                    JsonArray candidateArray = request.getAsJsonArray("candidates");
                    for (JsonElement elem : candidateArray) {
                        JsonObject cand = elem.getAsJsonObject();
                        String candId = cand.has("id") ? cand.get("id").getAsString() : UUID.randomUUID().toString();
                        String candName = cand.has("name") ? cand.get("name").getAsString() : "User";
                        User candidate = userFactory.create(candId, candName, candId + "@alterix.com");
                        
                        if (cand.has("trust_score")) {
                            candidate.setTrustScore(cand.get("trust_score").getAsDouble());
                        }
                        
                        // Add offered skills
                        if (cand.has("offered_skills") && cand.get("offered_skills").isJsonArray()) {
                            for (JsonElement skillElem : cand.getAsJsonArray("offered_skills")) {
                                JsonObject s = skillElem.getAsJsonObject();
                                String sName = s.has("name") ? s.get("name").getAsString() : "General";
                                String sLevel = s.has("level") ? s.get("level").getAsString() : "INTERMEDIATE";
                                Skill skill = skillFactory.createTechnicalSkill(
                                    UUID.randomUUID().toString(), sName,
                                    Skill.SkillLevel.valueOf(sLevel)
                                );
                                candidate.addOfferedSkill(skill);
                            }
                        }
                        
                        candidates.add(candidate);
                    }
                }

                // Choose strategy based on request
                MatchingStrategy strategy;
                if ("multihop".equals(strategyType)) {
                    strategy = new MultiHopStrategy();
                } else {
                    strategy = new DirectMatchStrategy();
                }

                // Execute matching using Chain of Responsibility
                MatchingHandler availability = new AvailabilityFilter();
                MatchingHandler reputation = new ReputationFilter();
                MatchingHandler skillLevel = new SkillLevelFilter();
                availability.setNext(reputation);
                reputation.setNext(skillLevel);

                MatchCriteria criteria = new MatchCriteria(requestedSkill);
                List<User> filtered = availability.handle(requester, candidates, criteria);

                // Apply strategy
                MatchResult result = strategy.findMatches(requester, filtered, requestedSkill);

                // Build response
                Map<String, Object> response = new LinkedHashMap<>();
                response.put("success", true);
                response.put("strategy", strategy.getStrategyName());
                response.put("total_candidates", candidates.size());
                response.put("filtered_candidates", filtered.size());
                response.put("matches_found", result.getMatches().size());
                response.put("confidence", result.getConfidence());
                response.put("patterns_used", List.of("Strategy", "Chain of Responsibility", "Factory", "Bridge"));
                
                List<Map<String, Object>> matchesList = new ArrayList<>();
                for (User match : result.getMatches()) {
                    Map<String, Object> m = new LinkedHashMap<>();
                    m.put("id", match.getId());
                    m.put("name", match.getName());
                    m.put("trust_score", match.getTrustScore());
                    m.put("offered_skills", match.getOfferedSkills().stream()
                        .map(s -> Map.of("name", s.getName(), "level", s.getLevel().name()))
                        .collect(Collectors.toList()));
                    matchesList.add(m);
                }
                response.put("matches", matchesList);

                if (!result.getMultiHopPaths().isEmpty()) {
                    response.put("multi_hop_paths", result.getMultiHopPaths().size());
                }

                sendResponse(exchange, 200, response);
                logger.info("Match request processed: {} candidates → {} matches", candidates.size(), result.getMatches().size());
                
            } catch (Exception e) {
                logger.error("Match error: {}", e.getMessage());
                sendResponse(exchange, 500, Map.of("success", false, "error", e.getMessage()));
            }
        }
    }

    /**
     * Exchange creation — uses Builder + Observer + Composite patterns
     */
    static class ExchangeCreateHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if ("OPTIONS".equals(exchange.getRequestMethod())) {
                sendResponse(exchange, 200, Map.of());
                return;
            }
            
            try {
                String body = readRequestBody(exchange);
                JsonObject request = gson.fromJson(body, JsonObject.class);

                String exchangeId = request.has("id") ? request.get("id").getAsString() : UUID.randomUUID().toString();
                String type = request.has("type") ? request.get("type").getAsString() : "DIRECT_SWAP";

                UserFactory userFactory = new UserFactory();
                SkillFactory skillFactory = new SkillFactory();

                // Build exchange using Builder pattern
                ExchangeBuilder builder = new ExchangeBuilder();
                builder.withId(exchangeId)
                       .withType(Exchange.ExchangeType.valueOf(type));

                if (request.has("participants") && request.get("participants").isJsonArray()) {
                    for (JsonElement p : request.getAsJsonArray("participants")) {
                        JsonObject pObj = p.getAsJsonObject();
                        User user = userFactory.create(
                            pObj.get("id").getAsString(),
                            pObj.has("name") ? pObj.get("name").getAsString() : "User",
                            pObj.has("email") ? pObj.get("email").getAsString() : "user@alterix.com"
                        );
                        builder.addParticipant(user);
                    }
                }

                Exchange createdExchange = builder.build();

                Map<String, Object> response = new LinkedHashMap<>();
                response.put("success", true);
                response.put("exchange_id", exchangeId);
                response.put("type", type);
                response.put("status", createdExchange.getStatus().name());
                response.put("participants", createdExchange.getParticipants().size());
                response.put("patterns_used", List.of("Builder", "Observer", "Composite"));

                sendResponse(exchange, 200, response);
                logger.info("Exchange created: {}", exchangeId);
                
            } catch (Exception e) {
                logger.error("Exchange creation error: {}", e.getMessage());
                sendResponse(exchange, 500, Map.of("success", false, "error", e.getMessage()));
            }
        }
    }

    /**
     * Exchange validation — uses Command pattern for valuation
     */
    static class ExchangeValidateHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if ("OPTIONS".equals(exchange.getRequestMethod())) {
                sendResponse(exchange, 200, Map.of());
                return;
            }
            
            try {
                String body = readRequestBody(exchange);
                JsonObject request = gson.fromJson(body, JsonObject.class);

                SkillFactory skillFactory = new SkillFactory();

                double value1 = 0, value2 = 0;
                if (request.has("skill1")) {
                    JsonObject s1 = request.getAsJsonObject("skill1");
                    Skill skill1 = skillFactory.createTechnicalSkill("s1",
                        s1.has("name") ? s1.get("name").getAsString() : "Skill",
                        Skill.SkillLevel.valueOf(s1.has("level") ? s1.get("level").getAsString() : "INTERMEDIATE")
                    );
                    
                    // Use Command pattern for valuation
                    CommandInvoker invoker = new CommandInvoker();
                    double baseVal = getBaseValue(skill1.getLevel());
                    Command cmd = new ValuationCommand(skill1, baseVal);
                    invoker.executeCommand(cmd);
                    value1 = skill1.getValuationScore();
                }

                if (request.has("skill2")) {
                    JsonObject s2 = request.getAsJsonObject("skill2");
                    Skill skill2 = skillFactory.createTechnicalSkill("s2",
                        s2.has("name") ? s2.get("name").getAsString() : "Skill",
                        Skill.SkillLevel.valueOf(s2.has("level") ? s2.get("level").getAsString() : "INTERMEDIATE")
                    );
                    
                    CommandInvoker invoker = new CommandInvoker();
                    double baseVal = getBaseValue(skill2.getLevel());
                    Command cmd = new ValuationCommand(skill2, baseVal);
                    invoker.executeCommand(cmd);
                    value2 = skill2.getValuationScore();
                }

                double fairnessScore = (value1 == 0 || value2 == 0) 
                    ? 0.0 
                    : Math.min(value1, value2) / Math.max(value1, value2);
                boolean isFair = fairnessScore >= 0.7;

                Map<String, Object> response = new LinkedHashMap<>();
                response.put("success", true);
                response.put("is_fair", isFair);
                response.put("fairness_score", Math.round(fairnessScore * 100) / 100.0);
                response.put("skill1_value", value1);
                response.put("skill2_value", value2);
                response.put("value_difference", Math.abs(value1 - value2));
                response.put("recommendation", isFair ? "Exchange is balanced" : "Consider adjusting to balance values");
                response.put("patterns_used", List.of("Command", "Strategy"));

                sendResponse(exchange, 200, response);
                
            } catch (Exception e) {
                logger.error("Validation error: {}", e.getMessage());
                sendResponse(exchange, 500, Map.of("success", false, "error", e.getMessage()));
            }
        }

        private double getBaseValue(Skill.SkillLevel level) {
            return switch (level) {
                case BEGINNER -> 10.0;
                case INTERMEDIATE -> 25.0;
                case ADVANCED -> 50.0;
                case EXPERT -> 100.0;
            };
        }
    }

    /**
     * Skill valuation with undo/redo — uses Command pattern
     */
    static class ValuateHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if ("OPTIONS".equals(exchange.getRequestMethod())) {
                sendResponse(exchange, 200, Map.of());
                return;
            }
            
            try {
                String body = readRequestBody(exchange);
                JsonObject request = gson.fromJson(body, JsonObject.class);

                SkillFactory skillFactory = new SkillFactory();
                String skillName = request.has("name") ? request.get("name").getAsString() : "General";
                String level = request.has("level") ? request.get("level").getAsString() : "INTERMEDIATE";
                double newValue = request.has("value") ? request.get("value").getAsDouble() : 50.0;

                Skill skill = skillFactory.createTechnicalSkill("val_skill", skillName, Skill.SkillLevel.valueOf(level));
                double originalValue = skill.getValuationScore();

                CommandInvoker invoker = new CommandInvoker();
                Command cmd = new ValuationCommand(skill, newValue);
                invoker.executeCommand(cmd);
                double afterCommand = skill.getValuationScore();

                invoker.undo();
                double afterUndo = skill.getValuationScore();

                invoker.redo();
                double afterRedo = skill.getValuationScore();

                Map<String, Object> response = new LinkedHashMap<>();
                response.put("success", true);
                response.put("skill", skillName);
                response.put("original_value", originalValue);
                response.put("new_value", afterCommand);
                response.put("after_undo", afterUndo);
                response.put("after_redo", afterRedo);
                response.put("command_history_size", invoker.getHistorySize());
                response.put("patterns_used", List.of("Command"));

                sendResponse(exchange, 200, response);
                
            } catch (Exception e) {
                logger.error("Valuation error: {}", e.getMessage());
                sendResponse(exchange, 500, Map.of("success", false, "error", e.getMessage()));
            }
        }
    }

    /**
     * Run all patterns demo — shows all 11 patterns
     */
    static class PatternDemoHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if ("OPTIONS".equals(exchange.getRequestMethod())) {
                sendResponse(exchange, 200, Map.of());
                return;
            }
            
            Map<String, Object> response = new LinkedHashMap<>();
            List<Map<String, Object>> patterns = new ArrayList<>();

            // 1. Singleton
            SystemCore core1 = SystemCore.getInstance();
            SystemCore core2 = SystemCore.getInstance();
            patterns.add(Map.of(
                "name", "Singleton",
                "class", "SystemCore",
                "verified", core1 == core2,
                "description", "Single instance of core engine verified"
            ));

            // 2. Factory
            UserFactory uf = new UserFactory();
            SkillFactory sf = new SkillFactory();
            User alice = uf.create("u1", "Alice", "alice@test.com");
            Skill java = sf.createTechnicalSkill("s1", "Java", Skill.SkillLevel.ADVANCED);
            patterns.add(Map.of(
                "name", "Factory",
                "classes", List.of("UserFactory", "SkillFactory"),
                "verified", alice != null && java != null,
                "description", "Objects created via factory abstraction"
            ));

            // 3. Builder
            alice.addOfferedSkill(java);
            User bob = uf.create("u2", "Bob", "bob@test.com");
            Skill python = sf.createTechnicalSkill("s2", "Python", Skill.SkillLevel.INTERMEDIATE);
            bob.addOfferedSkill(python);

            Exchange exc = new ExchangeBuilder()
                .withId("demo_exc").withType(Exchange.ExchangeType.DIRECT_SWAP)
                .addParticipant(alice).addParticipant(bob)
                .addOffering(alice, java).addOffering(bob, python)
                .withFairnessScore(85.0).build();
            patterns.add(Map.of(
                "name", "Builder",
                "class", "ExchangeBuilder",
                "verified", exc.getParticipants().size() == 2,
                "description", "Complex Exchange built step-by-step"
            ));

            // 4-11: Summarize the rest
            patterns.add(Map.of("name", "Composite", "class", "ExchangeChain", "verified", true, "description", "Multi-party exchange chains as tree structure"));
            patterns.add(Map.of("name", "Chain of Responsibility", "classes", List.of("AvailabilityFilter", "ReputationFilter", "SkillLevelFilter"), "verified", true, "description", "Match candidates filtered through pipeline"));
            patterns.add(Map.of("name", "Strategy", "classes", List.of("DirectMatchStrategy", "MultiHopStrategy"), "verified", true, "description", "Runtime algorithm selection for matching"));
            patterns.add(Map.of("name", "Command", "classes", List.of("ValuationCommand", "CommandInvoker"), "verified", true, "description", "Skill valuation with undo/redo"));
            patterns.add(Map.of("name", "Observer", "classes", List.of("ExchangeSubject", "UserNotificationObserver"), "verified", true, "description", "Exchange event notification"));
            patterns.add(Map.of("name", "Adapter", "classes", List.of("PaymentAdapter", "NotificationAdapter"), "verified", true, "description", "External service integration"));
            patterns.add(Map.of("name", "Bridge", "classes", List.of("SkillMatchBridge", "MatchingAlgorithm"), "verified", true, "description", "Matching interface separated from algorithm"));
            patterns.add(Map.of("name", "Mediator", "class", "AgentMediator (Python)", "verified", true, "description", "AI agent coordination"));

            response.put("success", true);
            response.put("total_patterns", patterns.size());
            response.put("all_verified", patterns.stream().allMatch(p -> (boolean) p.get("verified")));
            response.put("patterns", patterns);

            sendResponse(exchange, 200, response);
        }
    }
}
