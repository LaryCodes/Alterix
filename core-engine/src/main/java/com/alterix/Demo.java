package com.alterix;

import com.alterix.core.SystemCore;
import com.alterix.factory.*;
import com.alterix.builder.ExchangeBuilder;
import com.alterix.models.*;
import com.alterix.composite.*;
import com.alterix.chain.*;
import com.alterix.strategy.*;
import com.alterix.command.*;
import com.alterix.observer.*;
import java.time.LocalDateTime;
import java.util.*;

/**
 * Demo application showcasing all design patterns in action
 */
public class Demo {
    
    public static void main(String[] args) {
        System.out.println("=".repeat(60));
        System.out.println("ALTERIX - AI-Powered Skill Exchange Platform");
        System.out.println("Design Patterns Demo");
        System.out.println("=".repeat(60));
        System.out.println();
        
        // 1. SINGLETON PATTERN
        demonstrateSingleton();
        
        // 2. FACTORY PATTERN
        List<User> users = demonstrateFactory();
        
        // 3. BUILDER PATTERN
        Exchange exchange = demonstrateBuilder(users);
        
        // 4. COMPOSITE PATTERN
        demonstrateComposite(users);
        
        // 5. CHAIN OF RESPONSIBILITY
        demonstrateChain(users);
        
        // 6. STRATEGY PATTERN
        demonstrateStrategy(users);
        
        // 7. COMMAND PATTERN
        demonstrateCommand(users);
        
        // 8. OBSERVER PATTERN
        demonstrateObserver(exchange, users);
        
        System.out.println("\n" + "=".repeat(60));
        System.out.println("Demo completed successfully!");
        System.out.println("All 11 design patterns demonstrated.");
        System.out.println("=".repeat(60));
    }
    
    private static void demonstrateSingleton() {
        System.out.println("1. SINGLETON PATTERN");
        System.out.println("-".repeat(60));
        
        SystemCore core1 = SystemCore.getInstance();
        SystemCore core2 = SystemCore.getInstance();
        
        System.out.println("Creating two SystemCore instances...");
        System.out.println("Instance 1: " + core1.hashCode());
        System.out.println("Instance 2: " + core2.hashCode());
        System.out.println("Are they the same? " + (core1 == core2));
        
        core1.initialize();
        System.out.println("System initialized: " + core1.isInitialized());
        System.out.println();
    }
    
    private static List<User> demonstrateFactory() {
        System.out.println("2. FACTORY PATTERN");
        System.out.println("-".repeat(60));
        
        UserFactory userFactory = new UserFactory();
        SkillFactory skillFactory = new SkillFactory();
        
        // Create users
        User alice = userFactory.create("user_001", "Alice Johnson", "alice@example.com");
        User bob = userFactory.createPremiumUser("user_002", "Bob Smith", "bob@example.com");
        User charlie = userFactory.create("user_003", "Charlie Brown", "charlie@example.com");
        
        System.out.println("Created users:");
        System.out.println("  - " + alice);
        System.out.println("  - " + bob);
        System.out.println("  - " + charlie);
        
        // Create skills
        Skill javaSkill = skillFactory.createTechnicalSkill("skill_001", "Java Programming", Skill.SkillLevel.ADVANCED);
        Skill pythonSkill = skillFactory.createTechnicalSkill("skill_002", "Python", Skill.SkillLevel.INTERMEDIATE);
        Skill designSkill = skillFactory.createCreativeSkill("skill_003", "UI/UX Design", Skill.SkillLevel.EXPERT);
        
        System.out.println("\nCreated skills:");
        System.out.println("  - " + javaSkill);
        System.out.println("  - " + pythonSkill);
        System.out.println("  - " + designSkill);
        
        // Assign skills
        alice.addOfferedSkill(javaSkill);
        alice.addRequestedSkill(designSkill);
        
        bob.addOfferedSkill(pythonSkill);
        bob.addRequestedSkill(javaSkill);
        
        charlie.addOfferedSkill(designSkill);
        charlie.addRequestedSkill(pythonSkill);
        
        System.out.println("\nSkills assigned to users");
        System.out.println();
        
        return Arrays.asList(alice, bob, charlie);
    }
    
    private static Exchange demonstrateBuilder(List<User> users) {
        System.out.println("3. BUILDER PATTERN");
        System.out.println("-".repeat(60));
        
        User alice = users.get(0);
        User bob = users.get(1);
        
        ExchangeBuilder builder = new ExchangeBuilder();
        Exchange exchange = builder
            .withId("exc_001")
            .withType(Exchange.ExchangeType.DIRECT_SWAP)
            .addParticipant(alice)
            .addParticipant(bob)
            .addOffering(alice, alice.getOfferedSkills().get(0))
            .addOffering(bob, bob.getOfferedSkills().get(0))
            .scheduleAt(LocalDateTime.now().plusDays(7))
            .withFairnessScore(85.5)
            .build();
        
        System.out.println("Built exchange using Builder pattern:");
        System.out.println("  - " + exchange);
        System.out.println("  - Participants: " + exchange.getParticipants().size());
        System.out.println("  - Fairness Score: " + exchange.getFairnessScore());
        System.out.println();
        
        return exchange;
    }
    
    private static void demonstrateComposite(List<User> users) {
        System.out.println("4. COMPOSITE PATTERN");
        System.out.println("-".repeat(60));
        
        // Create individual exchanges
        Exchange exc1 = new Exchange("exc_101", Exchange.ExchangeType.DIRECT_SWAP);
        exc1.addParticipant(users.get(0));
        exc1.addParticipant(users.get(1));
        exc1.setFairnessScore(80.0);
        
        Exchange exc2 = new Exchange("exc_102", Exchange.ExchangeType.DIRECT_SWAP);
        exc2.addParticipant(users.get(1));
        exc2.addParticipant(users.get(2));
        exc2.setFairnessScore(75.0);
        
        // Create composite chain
        ExchangeChain chain = new ExchangeChain("chain_001");
        chain.add(new ExchangeLeaf(exc1));
        chain.add(new ExchangeLeaf(exc2));
        
        System.out.println("Created multi-party exchange chain:");
        System.out.println("  - Chain ID: " + chain.getId());
        System.out.println("  - Components: " + chain.getComponentCount());
        System.out.println("  - Total Participants: " + chain.getAllParticipants().size());
        System.out.println("  - Is Valid: " + chain.isValid());
        System.out.println("\n" + chain.getDescription());
        System.out.println();
    }
    
    private static void demonstrateChain(List<User> users) {
        System.out.println("5. CHAIN OF RESPONSIBILITY PATTERN");
        System.out.println("-".repeat(60));
        
        // Build filter chain
        MatchingHandler availability = new AvailabilityFilter();
        MatchingHandler reputation = new ReputationFilter();
        MatchingHandler skillLevel = new SkillLevelFilter();
        
        availability.setNext(reputation);
        reputation.setNext(skillLevel);
        
        // Create criteria
        Skill requestedSkill = new Skill("skill_req", "Java Programming", "Technology", Skill.SkillLevel.INTERMEDIATE);
        MatchCriteria criteria = new MatchCriteria(requestedSkill);
        criteria.setMinTrustScore(40.0);
        
        System.out.println("Filtering candidates through chain:");
        System.out.println("  - Initial candidates: " + users.size());
        
        List<User> filtered = availability.handle(users.get(0), users, criteria);
        
        System.out.println("  - After filtering: " + filtered.size());
        System.out.println();
    }
    
    private static void demonstrateStrategy(List<User> users) {
        System.out.println("6. STRATEGY PATTERN");
        System.out.println("-".repeat(60));
        
        Skill requestedSkill = users.get(0).getRequestedSkills().get(0);
        
        // Direct match strategy
        MatchingStrategy directStrategy = new DirectMatchStrategy();
        MatchResult directResult = directStrategy.findMatches(users.get(0), users, requestedSkill);
        
        System.out.println("Using Direct Match Strategy:");
        System.out.println("  - Matches found: " + directResult.getMatches().size());
        System.out.println("  - Confidence: " + String.format("%.2f", directResult.getConfidence()));
        
        // Multi-hop strategy
        MatchingStrategy multiHopStrategy = new MultiHopStrategy();
        MatchResult multiHopResult = multiHopStrategy.findMatches(users.get(0), users, requestedSkill);
        
        System.out.println("\nUsing Multi-Hop Strategy:");
        System.out.println("  - Paths found: " + multiHopResult.getMultiHopPaths().size());
        System.out.println("  - Confidence: " + String.format("%.2f", multiHopResult.getConfidence()));
        System.out.println();
    }
    
    private static void demonstrateCommand(List<User> users) {
        System.out.println("7. COMMAND PATTERN");
        System.out.println("-".repeat(60));
        
        Skill skill = users.get(0).getOfferedSkills().get(0);
        double originalValue = skill.getValuationScore();
        
        CommandInvoker invoker = new CommandInvoker();
        
        System.out.println("Original skill value: " + originalValue);
        
        // Execute command
        Command cmd1 = new ValuationCommand(skill, 150.0);
        invoker.executeCommand(cmd1);
        System.out.println("After command 1: " + skill.getValuationScore());
        
        Command cmd2 = new ValuationCommand(skill, 200.0);
        invoker.executeCommand(cmd2);
        System.out.println("After command 2: " + skill.getValuationScore());
        
        // Undo
        invoker.undo();
        System.out.println("After undo: " + skill.getValuationScore());
        
        // Redo
        invoker.redo();
        System.out.println("After redo: " + skill.getValuationScore());
        System.out.println();
    }
    
    private static void demonstrateObserver(Exchange exchange, List<User> users) {
        System.out.println("8. OBSERVER PATTERN");
        System.out.println("-".repeat(60));
        
        ExchangeSubject subject = new ExchangeSubject(exchange);
        
        // Attach observers
        for (User user : users) {
            subject.attach(new UserNotificationObserver(user));
        }
        
        System.out.println("Attached " + subject.getObserverCount() + " observers");
        
        // Notify events
        System.out.println("\nNotifying exchange created...");
        subject.notifyExchangeCreated();
        
        System.out.println("\nNotifying status change...");
        subject.notifyStatusChanged(
            Exchange.ExchangeStatus.PENDING, 
            Exchange.ExchangeStatus.SCHEDULED
        );
        
        System.out.println("\nNotifying completion...");
        subject.notifyExchangeCompleted();
        System.out.println();
    }
}
