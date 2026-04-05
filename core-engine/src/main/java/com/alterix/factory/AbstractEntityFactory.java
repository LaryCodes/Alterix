package com.alterix.factory;

/**
 * FACTORY PATTERN
 * Abstract factory interface for creating domain entities
 */
public interface AbstractEntityFactory<T> {
    T create(String id, Object... params);
    T createDefault(String id);
    boolean validate(T entity);
}
