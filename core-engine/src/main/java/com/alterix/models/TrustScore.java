package com.alterix.models;

public class TrustScore {
    private double score;
    private int totalExchanges;
    private int successfulExchanges;
    private double averageRating;
    private int reportCount;

    public TrustScore() {
        this.score = 50.0; // Start at neutral
        this.totalExchanges = 0;
        this.successfulExchanges = 0;
        this.averageRating = 0.0;
        this.reportCount = 0;
    }

    public double getScore() { return score; }
    
    public void updateScore(double rating, boolean successful) {
        totalExchanges++;
        if (successful) successfulExchanges++;
        
        // Weighted calculation
        double successRate = (double) successfulExchanges / totalExchanges;
        double ratingWeight = rating / 5.0;
        double reportPenalty = Math.min(reportCount * 5, 30);
        
        this.score = (successRate * 40) + (ratingWeight * 60) - reportPenalty;
        this.score = Math.max(0, Math.min(100, this.score));
        
        // Update average rating
        this.averageRating = ((averageRating * (totalExchanges - 1)) + rating) / totalExchanges;
    }

    public void addReport() {
        this.reportCount++;
        updateScore(averageRating, false);
    }

    public int getTotalExchanges() { return totalExchanges; }
    public int getSuccessfulExchanges() { return successfulExchanges; }
    public double getAverageRating() { return averageRating; }
    public int getReportCount() { return reportCount; }
}
