package com.alterix.composite;

import com.alterix.models.*;
import java.util.List;

/**
 * COMPOSITE PATTERN
 * Component interface for building multi-party exchange trees
 * Allows treating individual exchanges and exchange chains uniformly
 */
public interface ExchangeComponent {
    String getId();
    void add(ExchangeComponent component);
    void remove(ExchangeComponent component);
    ExchangeComponent getChild(int index);
    List<ExchangeComponent> getChildren();
    
    List<User> getAllParticipants();
    double calculateTotalValue();
    boolean isValid();
    void execute();
    
    String getDescription();
}
