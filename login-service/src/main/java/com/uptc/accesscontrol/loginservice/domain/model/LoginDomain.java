package com.uptc.accesscontrol.loginservice.domain.model;

import java.time.LocalDateTime;

/**
 * Login Domain Entity - Pure business logic, no infrastructure dependencies
 * This is the core domain model representing user login information
 */
public class LoginDomain {

    private Long id;
    private Long userId;
    private String password;
    private Boolean isLocked;
    private Integer failedAttempts;
    private LocalDateTime lockTime;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    // Constructor completo
    public LoginDomain(Long id, Long userId, String password, Boolean isLocked, 
                       Integer failedAttempts, LocalDateTime lockTime, 
                       LocalDateTime createdAt, LocalDateTime updatedAt) {
        this.id = id;
        this.userId = userId;
        this.password = password;
        this.isLocked = isLocked != null ? isLocked : false;
        this.failedAttempts = failedAttempts != null ? failedAttempts : 0;
        this.lockTime = lockTime;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
    }

    // Constructor sin ID (para nuevas entidades)
    public LoginDomain(Long userId, String password) {
        this(null, userId, password, false, 0, null, LocalDateTime.now(), LocalDateTime.now());
    }

    // Constructor vacío
    public LoginDomain() {
        this.isLocked = false;
        this.failedAttempts = 0;
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }

    // Business Logic Methods

    /**
     * Check if the account is currently locked
     */
    public boolean isAccountLocked(int lockDurationMinutes) {
        if (!isLocked || lockTime == null) {
            return false;
        }
        
        LocalDateTime unlockTime = lockTime.plusMinutes(lockDurationMinutes);
        return LocalDateTime.now().isBefore(unlockTime);
    }

    /**
     * Calculate remaining lock time in minutes
     */
    public long getRemainingLockTimeMinutes(int lockDurationMinutes) {
        if (!isLocked || lockTime == null) {
            return 0;
        }
        
        LocalDateTime unlockTime = lockTime.plusMinutes(lockDurationMinutes);
        LocalDateTime now = LocalDateTime.now();
        
        if (now.isAfter(unlockTime)) {
            return 0;
        }
        
        return java.time.Duration.between(now, unlockTime).toMinutes();
    }

    /**
     * Increment failed login attempts
     */
    public void incrementFailedAttempts() {
        this.failedAttempts++;
        this.updatedAt = LocalDateTime.now();
    }

    /**
     * Reset failed attempts after successful login
     */
    public void resetFailedAttempts() {
        this.failedAttempts = 0;
        this.updatedAt = LocalDateTime.now();
    }

    /**
     * Lock the account
     */
    public void lock() {
        this.isLocked = true;
        this.lockTime = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }

    /**
     * Unlock the account
     */
    public void unlock() {
        this.isLocked = false;
        this.failedAttempts = 0;
        this.lockTime = null;
        this.updatedAt = LocalDateTime.now();
    }

    /**
     * Check if the account should be locked based on failed attempts
     */
    public boolean shouldBeLocked(int maxAttempts) {
        return this.failedAttempts >= maxAttempts;
    }

    /**
     * Update timestamp on modification
     */
    public void markAsUpdated() {
        this.updatedAt = LocalDateTime.now();
    }

    // Getters and Setters

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
        this.updatedAt = LocalDateTime.now();
    }

    public Boolean getIsLocked() {
        return isLocked;
    }

    public void setIsLocked(Boolean isLocked) {
        this.isLocked = isLocked;
    }

    public Integer getFailedAttempts() {
        return failedAttempts;
    }

    public void setFailedAttempts(Integer failedAttempts) {
        this.failedAttempts = failedAttempts;
    }

    public LocalDateTime getLockTime() {
        return lockTime;
    }

    public void setLockTime(LocalDateTime lockTime) {
        this.lockTime = lockTime;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(LocalDateTime updatedAt) {
        this.updatedAt = updatedAt;
    }

    @Override
    public String toString() {
        return "LoginDomain{" +
                "id=" + id +
                ", userId=" + userId +
                ", isLocked=" + isLocked +
                ", failedAttempts=" + failedAttempts +
                ", lockTime=" + lockTime +
                ", createdAt=" + createdAt +
                ", updatedAt=" + updatedAt +
                '}';
    }
}
