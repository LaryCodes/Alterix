package com.alterix.factory;

import com.alterix.models.User;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * FACTORY PATTERN
 * Creates User objects with validation and initialization logic
 */
public class UserFactory implements AbstractEntityFactory<User> {
    private static final Logger logger = LoggerFactory.getLogger(UserFactory.class);

    @Override
    public User create(String id, Object... params) {
        if (params.length < 2) {
            throw new IllegalArgumentException("UserFactory requires name and email");
        }
        
        String name = (String) params[0];
        String email = (String) params[1];
        
        if (!isValidEmail(email)) {
            throw new IllegalArgumentException("Invalid email format: " + email);
        }
        
        User user = new User(id, name, email);
        logger.info("Created user: {}", user.getId());
        return user;
    }

    @Override
    public User createDefault(String id) {
        return new User(id, "Anonymous User", "user@alterix.com");
    }

    @Override
    public boolean validate(User user) {
        return user != null 
            && user.getId() != null 
            && !user.getId().isEmpty()
            && user.getName() != null 
            && !user.getName().isEmpty()
            && isValidEmail(user.getEmail());
    }

    private boolean isValidEmail(String email) {
        return email != null && email.matches("^[A-Za-z0-9+_.-]+@(.+)$");
    }

    /**
     * Factory method for creating premium users with additional features
     */
    public User createPremiumUser(String id, String name, String email) {
        User user = create(id, name, email);
        user.setMetadata("premium", true);
        user.setMetadata("maxExchanges", 50);
        logger.info("Created premium user: {}", user.getId());
        return user;
    }

    /**
     * Factory method for creating verified users
     */
    public User createVerifiedUser(String id, String name, String email) {
        User user = create(id, name, email);
        user.setMetadata("verified", true);
        user.getTrustScore().updateScore(5.0, true);
        logger.info("Created verified user: {}", user.getId());
        return user;
    }
}
