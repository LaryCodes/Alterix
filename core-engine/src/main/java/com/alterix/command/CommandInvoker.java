package com.alterix.command;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.*;

/**
 * COMMAND PATTERN - Invoker
 * Manages command execution and history
 */
public class CommandInvoker {
    private static final Logger logger = LoggerFactory.getLogger(CommandInvoker.class);
    
    private final Stack<Command> executedCommands;
    private final Stack<Command> undoneCommands;

    public CommandInvoker() {
        this.executedCommands = new Stack<>();
        this.undoneCommands = new Stack<>();
    }

    public void executeCommand(Command command) {
        command.execute();
        executedCommands.push(command);
        undoneCommands.clear(); // Clear redo history
        logger.info("Executed command: {}", command.getDescription());
    }

    public void undo() {
        if (executedCommands.isEmpty()) {
            logger.warn("No commands to undo");
            return;
        }
        
        Command command = executedCommands.pop();
        command.undo();
        undoneCommands.push(command);
        logger.info("Undone command: {}", command.getDescription());
    }

    public void redo() {
        if (undoneCommands.isEmpty()) {
            logger.warn("No commands to redo");
            return;
        }
        
        Command command = undoneCommands.pop();
        command.execute();
        executedCommands.push(command);
        logger.info("Redone command: {}", command.getDescription());
    }

    public List<String> getCommandHistory() {
        List<String> history = new ArrayList<>();
        for (Command cmd : executedCommands) {
            history.add(cmd.getDescription());
        }
        return history;
    }

    public void clearHistory() {
        executedCommands.clear();
        undoneCommands.clear();
        logger.info("Command history cleared");
    }

    public boolean canUndo() {
        return !executedCommands.isEmpty();
    }

    public boolean canRedo() {
        return !undoneCommands.isEmpty();
    }

    public int getHistorySize() {
        return executedCommands.size();
    }
}
