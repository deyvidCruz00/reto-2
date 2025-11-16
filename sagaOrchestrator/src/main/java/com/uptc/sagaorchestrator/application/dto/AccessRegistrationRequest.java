package com.uptc.sagaorchestrator.application.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AccessRegistrationRequest {
    private String sagaId;
    private String employeeId;
    private String employeeName;
    private String action; // CHECK_IN or CHECK_OUT
}
