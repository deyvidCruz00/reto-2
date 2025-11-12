package com.uptc.accesscontrol.loginservice.infrastructure.event;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AlertEvent {
    
    private String alertId;
    private LocalDateTime timestamp;
    private String description;
    private String code;
    private Long userId;
    private String severity;
}
