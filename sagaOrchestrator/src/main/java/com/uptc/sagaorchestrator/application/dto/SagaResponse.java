package com.uptc.sagaorchestrator.application.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SagaResponse {
    private String sagaId;
    private String type;
    private String status;
    private String employeeId;
    private String employeeName;
    private String accessId;
    private String errorMessage;
    private LocalDateTime createdAt;
    private LocalDateTime completedAt;
}
