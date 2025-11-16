package com.uptc.sagaorchestrator.domain.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Table(name = "saga_steps")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SagaStep {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "saga_id", nullable = false)
    private Saga saga;
    
    @Column(nullable = false)
    private Integer stepNumber;
    
    @Column(nullable = false)
    private String stepName;
    
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private StepStatus status;
    
    @Column(columnDefinition = "TEXT")
    private String request;
    
    @Column(columnDefinition = "TEXT")
    private String response;
    
    @Column(columnDefinition = "TEXT")
    private String errorMessage;
    
    @Column(nullable = false)
    private LocalDateTime startedAt;
    
    private LocalDateTime completedAt;
    
    private Boolean compensated;
    
    @PrePersist
    protected void onCreate() {
        if (startedAt == null) {
            startedAt = LocalDateTime.now();
        }
        if (status == null) {
            status = StepStatus.PENDING;
        }
        if (compensated == null) {
            compensated = false;
        }
    }
    
    public void complete(String response) {
        this.status = StepStatus.COMPLETED;
        this.response = response;
        this.completedAt = LocalDateTime.now();
    }
    
    public void fail(String errorMessage) {
        this.status = StepStatus.FAILED;
        this.errorMessage = errorMessage;
        this.completedAt = LocalDateTime.now();
    }
    
    public void compensate() {
        this.compensated = true;
    }
    
    public enum StepStatus {
        PENDING,
        IN_PROGRESS,
        COMPLETED,
        FAILED,
        SKIPPED
    }
}
