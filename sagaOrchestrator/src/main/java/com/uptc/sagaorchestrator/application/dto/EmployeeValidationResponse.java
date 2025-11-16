package com.uptc.sagaorchestrator.application.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class EmployeeValidationResponse {
    private String sagaId;
    private Boolean isValid;
    private String employeeName;
    private String errorMessage;
}
