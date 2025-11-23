package com.uptc.alertservice.domain.entity;

import java.time.LocalDateTime;

/**
 * Alert Domain Entity - Pure business logic, no infrastructure dependencies
 * This is the core domain model representing an alert
 */
public class AlertDomain {
    
    private Long id;
    private LocalDateTime timestamp;
    private String description;
    private String code;
    private String severity;
    private String employeeId;
    private String userId;
    private String additionalInfo;
    
    // Constructor completo
    public AlertDomain(Long id, LocalDateTime timestamp, String description, String code,
                       String severity, String employeeId, String userId, String additionalInfo) {
        this.id = id;
        this.timestamp = timestamp != null ? timestamp : LocalDateTime.now();
        this.description = description;
        this.code = code;
        this.severity = severity != null ? severity : "INFO";
        this.employeeId = employeeId;
        this.userId = userId;
        this.additionalInfo = additionalInfo;
    }
    
    // Constructor simplificado
    public AlertDomain(String code, String description, String severity) {
        this(null, LocalDateTime.now(), description, code, severity, null, null, null);
    }
    
    // Constructor vacío
    public AlertDomain() {
        this.timestamp = LocalDateTime.now();
        this.severity = "INFO";
    }
    
    // Business Logic Methods
    
    /**
     * Check if alert is critical
     */
    public boolean isCritical() {
        return "CRITICAL".equalsIgnoreCase(this.severity);
    }
    
    /**
     * Check if alert is a warning or higher
     */
    public boolean isWarningOrHigher() {
        return "WARNING".equalsIgnoreCase(this.severity) || 
               "ERROR".equalsIgnoreCase(this.severity) || 
               "CRITICAL".equalsIgnoreCase(this.severity);
    }
    
    /**
     * Check if alert is recent (within last hour)
     */
    public boolean isRecent() {
        if (timestamp == null) {
            return false;
        }
        LocalDateTime oneHourAgo = LocalDateTime.now().minusHours(1);
        return timestamp.isAfter(oneHourAgo);
    }
    
    /**
     * Get alert age in hours
     */
    public long getAgeInHours() {
        if (timestamp == null) {
            return 0;
        }
        return java.time.Duration.between(timestamp, LocalDateTime.now()).toHours();
    }
    
    /**
     * Validate alert has required fields
     */
    public boolean isValid() {
        return code != null && !code.trim().isEmpty() &&
               description != null && !description.trim().isEmpty() &&
               severity != null && !severity.trim().isEmpty();
    }
    
    /**
     * Get severity priority (higher number = more severe)
     */
    public int getSeverityPriority() {
        if (severity == null) return 0;
        
        switch (severity.toUpperCase()) {
            case "CRITICAL": return 4;
            case "ERROR": return 3;
            case "WARNING": return 2;
            case "INFO": return 1;
            default: return 0;
        }
    }
    
    // Getters and Setters
    
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public LocalDateTime getTimestamp() {
        return timestamp;
    }
    
    public void setTimestamp(LocalDateTime timestamp) {
        this.timestamp = timestamp;
    }
    
    public String getDescription() {
        return description;
    }
    
    public void setDescription(String description) {
        this.description = description;
    }
    
    public String getCode() {
        return code;
    }
    
    public void setCode(String code) {
        this.code = code;
    }
    
    public String getSeverity() {
        return severity;
    }
    
    public void setSeverity(String severity) {
        this.severity = severity;
    }
    
    public String getEmployeeId() {
        return employeeId;
    }
    
    public void setEmployeeId(String employeeId) {
        this.employeeId = employeeId;
    }
    
    public String getUserId() {
        return userId;
    }
    
    public void setUserId(String userId) {
        this.userId = userId;
    }
    
    public String getAdditionalInfo() {
        return additionalInfo;
    }
    
    public void setAdditionalInfo(String additionalInfo) {
        this.additionalInfo = additionalInfo;
    }
    
    @Override
    public String toString() {
        return "AlertDomain{" +
                "id=" + id +
                ", timestamp=" + timestamp +
                ", code='" + code + '\'' +
                ", severity='" + severity + '\'' +
                ", description='" + description + '\'' +
                ", employeeId='" + employeeId + '\'' +
                '}';
    }
}
