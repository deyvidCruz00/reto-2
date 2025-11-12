package com.uptc.alertservice.infrastructure.rest;

import com.uptc.alertservice.application.dto.AlertRequest;
import com.uptc.alertservice.application.dto.AlertResponse;
import com.uptc.alertservice.domain.entity.Alert;
import com.uptc.alertservice.domain.port.AlertUseCasePort;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/alert")
@RequiredArgsConstructor
@Slf4j
@Tag(name = "Alert", description = "Alert management endpoints")
public class AlertController {
    
    private final AlertUseCasePort alertUseCase;
    
    @PostMapping("/create")
    @Operation(summary = "Create a new alert manually")
    public ResponseEntity<AlertResponse> createAlert(@RequestBody AlertRequest request) {
        log.info("Creating alert manually: {}", request.getCode());
        Alert alert = alertUseCase.createAlert(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(toResponse(alert));
    }
    
    @GetMapping("/{id}")
    @Operation(summary = "Get alert by ID")
    public ResponseEntity<AlertResponse> getAlertById(@PathVariable Long id) {
        log.info("Fetching alert by ID: {}", id);
        Alert alert = alertUseCase.getAlertById(id);
        return ResponseEntity.ok(toResponse(alert));
    }
    
    @GetMapping("/all")
    @Operation(summary = "Get all alerts")
    public ResponseEntity<List<AlertResponse>> getAllAlerts() {
        log.info("Fetching all alerts");
        List<Alert> alerts = alertUseCase.getAllAlerts();
        List<AlertResponse> responses = alerts.stream()
                .map(this::toResponse)
                .collect(Collectors.toList());
        return ResponseEntity.ok(responses);
    }
    
    @GetMapping("/code/{code}")
    @Operation(summary = "Get alerts by code")
    public ResponseEntity<List<AlertResponse>> getAlertsByCode(@PathVariable String code) {
        log.info("Fetching alerts by code: {}", code);
        List<Alert> alerts = alertUseCase.getAlertsByCode(code);
        List<AlertResponse> responses = alerts.stream()
                .map(this::toResponse)
                .collect(Collectors.toList());
        return ResponseEntity.ok(responses);
    }
    
    @GetMapping("/severity/{severity}")
    @Operation(summary = "Get alerts by severity")
    public ResponseEntity<List<AlertResponse>> getAlertsBySeverity(@PathVariable String severity) {
        log.info("Fetching alerts by severity: {}", severity);
        List<Alert> alerts = alertUseCase.getAlertsBySeverity(severity);
        List<AlertResponse> responses = alerts.stream()
                .map(this::toResponse)
                .collect(Collectors.toList());
        return ResponseEntity.ok(responses);
    }
    
    @GetMapping("/employee/{employeeId}")
    @Operation(summary = "Get alerts by employee ID")
    public ResponseEntity<List<AlertResponse>> getAlertsByEmployeeId(@PathVariable String employeeId) {
        log.info("Fetching alerts by employee ID: {}", employeeId);
        List<Alert> alerts = alertUseCase.getAlertsByEmployeeId(employeeId);
        List<AlertResponse> responses = alerts.stream()
                .map(this::toResponse)
                .collect(Collectors.toList());
        return ResponseEntity.ok(responses);
    }
    
    @GetMapping("/daterange")
    @Operation(summary = "Get alerts by date range")
    public ResponseEntity<List<AlertResponse>> getAlertsByDateRange(
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime start,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime end) {
        log.info("Fetching alerts between {} and {}", start, end);
        List<Alert> alerts = alertUseCase.getAlertsByDateRange(start, end);
        List<AlertResponse> responses = alerts.stream()
                .map(this::toResponse)
                .collect(Collectors.toList());
        return ResponseEntity.ok(responses);
    }
    
    @GetMapping("/stats/total")
    @Operation(summary = "Get total alert count")
    public ResponseEntity<Long> getTotalAlerts() {
        long count = alertUseCase.getTotalAlerts();
        return ResponseEntity.ok(count);
    }
    
    @GetMapping("/stats/code/{code}")
    @Operation(summary = "Get alert count by code")
    public ResponseEntity<Long> getAlertCountByCode(@PathVariable String code) {
        long count = alertUseCase.getAlertCountByCode(code);
        return ResponseEntity.ok(count);
    }
    
    @GetMapping("/stats/severity/{severity}")
    @Operation(summary = "Get alert count by severity")
    public ResponseEntity<Long> getAlertCountBySeverity(@PathVariable String severity) {
        long count = alertUseCase.getAlertCountBySeverity(severity);
        return ResponseEntity.ok(count);
    }
    
    @GetMapping("/health")
    @Operation(summary = "Health check")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok("Alert Service is UP");
    }
    
    private AlertResponse toResponse(Alert alert) {
        return AlertResponse.builder()
                .id(alert.getId())
                .code(alert.getCode())
                .description(alert.getDescription())
                .severity(alert.getSeverity())
                .employeeId(alert.getEmployeeId())
                .userId(alert.getUserId())
                .timestamp(alert.getTimestamp())
                .additionalInfo(alert.getAdditionalInfo())
                .build();
    }
}
