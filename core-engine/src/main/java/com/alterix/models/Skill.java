package com.alterix.models;

public class Skill {
    private final String id;
    private String name;
    private String category;
    private SkillLevel level;
    private int estimatedHours;
    private double valuationScore;
    private String description;

    public enum SkillLevel {
        BEGINNER, INTERMEDIATE, ADVANCED, EXPERT
    }

    public Skill(String id, String name, String category, SkillLevel level) {
        this.id = id;
        this.name = name;
        this.category = category;
        this.level = level;
        this.estimatedHours = 0;
        this.valuationScore = 0.0;
    }

    public String getId() { return id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }
    
    public SkillLevel getLevel() { return level; }
    public void setLevel(SkillLevel level) { this.level = level; }
    
    public int getEstimatedHours() { return estimatedHours; }
    public void setEstimatedHours(int hours) { this.estimatedHours = hours; }
    
    public double getValuationScore() { return valuationScore; }
    public void setValuationScore(double score) { this.valuationScore = score; }
    
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    @Override
    public String toString() {
        return "Skill{name='" + name + "', level=" + level + ", value=" + valuationScore + "}";
    }
}
