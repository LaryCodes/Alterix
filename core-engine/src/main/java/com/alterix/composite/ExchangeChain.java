package com.alterix.composite;

import com.alterix.models.User;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.*;
import java.util.stream.Collectors;

/**
 * COMPOSITE PATTERN - Composite
 * Represents a multi-party exchange chain (A → B → C → D)
 * Can contain multiple exchanges forming a chain
 */
public class ExchangeChain implements ExchangeComponent {
    private static final Logger logger = LoggerFactory.getLogger(ExchangeChain.class);
    
    private final String id;
    private final List<ExchangeComponent> components;
    private String description;

    public ExchangeChain(String id) {
        this.id = id;
        this.components = new ArrayList<>();
        this.description = "Multi-party exchange chain";
    }

    @Override
    public String getId() {
        return id;
    }

    @Override
    public void add(ExchangeComponent component) {
        if (component == null) {
            throw new IllegalArgumentException("Cannot add null component");
        }
        components.add(component);
        logger.info("Added component to chain {}: {}", id, component.getId());
    }

    @Override
    public void remove(ExchangeComponent component) {
        components.remove(component);
        logger.info("Removed component from chain {}: {}", id, component.getId());
    }

    @Override
    public ExchangeComponent getChild(int index) {
        if (index < 0 || index >= components.size()) {
            throw new IndexOutOfBoundsException("Invalid child index: " + index);
        }
        return components.get(index);
    }

    @Override
    public List<ExchangeComponent> getChildren() {
        return new ArrayList<>(components);
    }

    @Override
    public List<User> getAllParticipants() {
        Set<User> allParticipants = new HashSet<>();
        for (ExchangeComponent component : components) {
            allParticipants.addAll(component.getAllParticipants());
        }
        return new ArrayList<>(allParticipants);
    }

    @Override
    public double calculateTotalValue() {
        return components.stream()
            .mapToDouble(ExchangeComponent::calculateTotalValue)
            .sum();
    }

    @Override
    public boolean isValid() {
        if (components.isEmpty()) {
            return false;
        }
        
        // All components must be valid
        boolean allValid = components.stream()
            .allMatch(ExchangeComponent::isValid);
        
        // Chain must be connected (each exchange shares participant with next)
        boolean isConnected = isChainConnected();
        
        return allValid && isConnected;
    }

    private boolean isChainConnected() {
        if (components.size() < 2) {
            return true;
        }
        
        for (int i = 0; i < components.size() - 1; i++) {
            List<User> currentParticipants = components.get(i).getAllParticipants();
            List<User> nextParticipants = components.get(i + 1).getAllParticipants();
            
            // Check if there's at least one common participant
            boolean hasCommon = currentParticipants.stream()
                .anyMatch(nextParticipants::contains);
            
            if (!hasCommon) {
                logger.warn("Chain {} is disconnected between components {} and {}", 
                    id, i, i + 1);
                return false;
            }
        }
        return true;
    }

    @Override
    public void execute() {
        if (!isValid()) {
            throw new IllegalStateException("Cannot execute invalid exchange chain");
        }
        
        logger.info("Executing exchange chain: {} with {} components", id, components.size());
        
        // Execute all exchanges in sequence
        for (ExchangeComponent component : components) {
            component.execute();
        }
        
        logger.info("Exchange chain {} completed successfully", id);
    }

    @Override
    public String getDescription() {
        StringBuilder sb = new StringBuilder();
        sb.append(String.format("ExchangeChain[%s]: %d components, %d total participants, value=%.2f\n",
            id, components.size(), getAllParticipants().size(), calculateTotalValue()));
        
        for (int i = 0; i < components.size(); i++) {
            sb.append(String.format("  [%d] %s\n", i, components.get(i).getDescription()));
        }
        
        return sb.toString();
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public int getComponentCount() {
        return components.size();
    }

    /**
     * Get the chain path as a list of user IDs
     */
    public List<String> getChainPath() {
        return getAllParticipants().stream()
            .map(User::getId)
            .collect(Collectors.toList());
    }
}
