package com.uptc.accesscontrol.loginservice.infrastructure.persistence;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * JPA Entity for Login - Infrastructure layer
 * This entity is used for database persistence only
 */
@Entity
@Table(name = "login")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class LoginJpaEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "user_id", nullable = false, unique = true)
    private Long userId;

    @Column(nullable = false)
    private String password;

    @Column(name = "is_locked")
    private Boolean isLocked;

    @Column(name = "failed_attempts")
    private Integer failedAttempts;

    @Column(name = "lock_time")
    private LocalDateTime lockTime;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() {
        if (createdAt == null) {
            createdAt = LocalDateTime.now();
        }
        if (updatedAt == null) {
            updatedAt = LocalDateTime.now();
        }
        if (isLocked == null) {
            isLocked = false;
        }
        if (failedAttempts == null) {
            failedAttempts = 0;
        }
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
}
