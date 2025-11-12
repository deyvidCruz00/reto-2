package com.uptc.alertservice.application.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AlertResponse {
    private Long id;
    private String code;
    private String description;
    private String severity;
    private String employeeId;
    private String userId;
    private LocalDateTime timestamp;
    private String additionalInfo;
}
