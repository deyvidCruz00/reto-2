package com.uptc.alertservice.domain.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Table(name = "alert", indexes = {
    @Index(name = "idx_alert_code", columnList = "code"),
    @Index(name = "idx_alert_timestamp", columnList = "timestamp"),
    @Index(name = "idx_alert_severity", columnList = "severity")
})
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Alert {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private LocalDateTime timestamp;
    
    @Column(nullable = false, length = 500)
    private String description;
    
    @Column(nullable = false, length = 100)
    private String code;
    
    @Column(nullable = false, length = 20)
    private String severity; // INFO, WARNING, ERROR, CRITICAL
    
    @Column(name = "employee_id", length = 50)
    private String employeeId;
    
    @Column(name = "user_id", length = 100)
    private String userId;
    
    @Column(name = "additional_info", columnDefinition = "TEXT")
    private String additionalInfo;
    
    @PrePersist
    protected void onCreate() {
        if (timestamp == null) {
            timestamp = LocalDateTime.now();
        }
        if (severity == null) {
            severity = "INFO";
        }
    }
}
