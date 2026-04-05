package com.alterix.factory;

import com.alterix.models.Skill;
import com.alterix.models.Skill.SkillLevel;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * FACTORY PATTERN
 * Creates Skill objects with category-specific initialization
 */
public class SkillFactory implements AbstractEntityFactory<Skill> {
    private static final Logger logger = LoggerFactory.getLogger(SkillFactory.class);

    @Override
    public Skill create(String id, Object... params) {
        if (params.length < 3) {
            throw new IllegalArgumentException("SkillFactory requires name, category, and level");
        }
        
        String name = (String) params[0];
        String category = (String) params[1];
        SkillLevel level = (SkillLevel) params[2];
        
        Skill skill = new Skill(id, name, category, level);
        
        // Set default valuation based on level
        skill.setValuationScore(calculateBaseValuation(level));
        
        logger.info("Created skill: {} ({})", skill.getName(), skill.getLevel());
        return skill;
    }

    @Override
    public Skill createDefault(String id) {
        return new Skill(id, "General Skill", "Other", SkillLevel.BEGINNER);
    }

    @Override
    public boolean validate(Skill skill) {
        return skill != null 
            && skill.getId() != null 
            && !skill.getId().isEmpty()
            && skill.getName() != null 
            && !skill.getName().isEmpty()
            && skill.getCategory() != null
            && skill.getLevel() != null;
    }

    private double calculateBaseValuation(SkillLevel level) {
        return switch (level) {
            case BEGINNER -> 10.0;
            case INTERMEDIATE -> 25.0;
            case ADVANCED -> 50.0;
            case EXPERT -> 100.0;
        };
    }

    /**
     * Factory method for creating technical skills with higher valuation
     */
    public Skill createTechnicalSkill(String id, String name, SkillLevel level) {
        Skill skill = create(id, name, "Technology", level);
        skill.setValuationScore(skill.getValuationScore() * 1.5);
        logger.info("Created technical skill: {}", skill.getName());
        return skill;
    }

    /**
     * Factory method for creating creative skills
     */
    public Skill createCreativeSkill(String id, String name, SkillLevel level) {
        Skill skill = create(id, name, "Creative", level);
        skill.setValuationScore(skill.getValuationScore() * 1.3);
        logger.info("Created creative skill: {}", skill.getName());
        return skill;
    }

    /**
     * Factory method for creating business skills
     */
    public Skill createBusinessSkill(String id, String name, SkillLevel level) {
        Skill skill = create(id, name, "Business", level);
        skill.setValuationScore(skill.getValuationScore() * 1.4);
        logger.info("Created business skill: {}", skill.getName());
        return skill;
    }
}
