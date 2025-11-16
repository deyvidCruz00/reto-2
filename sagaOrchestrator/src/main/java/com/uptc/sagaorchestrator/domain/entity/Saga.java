package com.uptc.sagaorchestrator.domain.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "sagas")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Saga {
    
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private String id;
    
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private SagaType type;
    
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private SagaStatus status;
    
    @Column(nullable = false)
    private String employeeId;
    
    private String employeeName;
    
    private String accessId;
    
    @Column(columnDefinition = "TEXT")
    private String errorMessage;
    
    @Column(nullable = false)
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private LocalDateTime completedAt;
    
    @OneToMany(mappedBy = "saga", cascade = CascadeType.ALL, orphanRemoval = true)
    @Builder.Default
    private List<SagaStep> steps = new ArrayList<>();
    
    @OneToMany(mappedBy = "saga", cascade = CascadeType.ALL, orphanRemoval = true)
    @Builder.Default
    private List<SagaLog> logs = new ArrayList<>();
    
    @Version
    private Long version;
    
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
        if (status == null) {
            status = SagaStatus.STARTED;
        }
    }
    
    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
    
    public void addStep(SagaStep step) {
        steps.add(step);
        step.setSaga(this);
    }
    
    public void addLog(SagaLog log) {
        logs.add(log);
        log.setSaga(this);
    }
    
    public void complete() {
        this.status = SagaStatus.COMPLETED;
        this.completedAt = LocalDateTime.now();
    }
    
    public void fail(String errorMessage) {
        this.status = SagaStatus.FAILED;
        this.errorMessage = errorMessage;
        this.completedAt = LocalDateTime.now();
    }
    
    public void compensate() {
        this.status = SagaStatus.COMPENSATING;
    }
    
    public void compensated() {
        this.status = SagaStatus.COMPENSATED;
        this.completedAt = LocalDateTime.now();
    }
    
    public enum SagaType {
        CHECK_IN,
        CHECK_OUT
    }
    
    public enum SagaStatus {
        STARTED,
        PENDING_EMPLOYEE_VALIDATION,
        EMPLOYEE_VALIDATED,
        PENDING_ACCESS_REGISTRATION,
        ACCESS_REGISTERED,
        COMPLETED,
        COMPENSATING,
        COMPENSATED,
        FAILED
    }
}
