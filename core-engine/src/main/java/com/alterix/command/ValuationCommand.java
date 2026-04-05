package com.alterix.command;

import com.alterix.models.Skill;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * COMMAND PATTERN - Concrete Command
 * Encapsulates skill valuation operation
 */
public class ValuationCommand implements Command {
    private static final Logger logger = LoggerFactory.getLogger(ValuationCommand.class);
    
    private final Skill skill;
    private final double newValuation;
    private double previousValuation;
    private boolean executed;

    public ValuationCommand(Skill skill, double newValuation) {
        this.skill = skill;
        this.newValuation = newValuation;
        this.executed = false;
    }

    @Override
    public void execute() {
        if (executed) {
            logger.warn("Command already executed for skill: {}", skill.getName());
            return;
        }
        
        previousValuation = skill.getValuationScore();
        skill.setValuationScore(newValuation);
        executed = true;
        
        logger.info("Updated valuation for {}: {} -> {}", 
            skill.getName(), previousValuation, newValuation);
    }

    @Override
    public void undo() {
        if (!executed) {
            logger.warn("Cannot undo: command not executed");
            return;
        }
        
        skill.setValuationScore(previousValuation);
        executed = false;
        
        logger.info("Reverted valuation for {}: {} -> {}", 
            skill.getName(), newValuation, previousValuation);
    }

    @Override
    public boolean isExecuted() {
        return executed;
    }

    @Override
    public String getDescription() {
        return String.format("Valuation command for %s: %.2f -> %.2f", 
            skill.getName(), previousValuation, newValuation);
    }

    public Skill getSkill() {
        return skill;
    }

    public double getNewValuation() {
        return newValuation;
    }
}
