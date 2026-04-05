package com.alterix.command;

/**
 * COMMAND PATTERN
 * Interface for encapsulating operations as objects
 */
public interface Command {
    void execute();
    void undo();
    boolean isExecuted();
    String getDescription();
}
