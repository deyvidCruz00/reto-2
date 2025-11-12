package com.uptc.alertservice.application.service;

import com.uptc.alertservice.application.dto.AlertRequest;
import com.uptc.alertservice.domain.entity.Alert;
import com.uptc.alertservice.domain.port.AlertRepositoryPort;
import com.uptc.alertservice.domain.port.AlertUseCasePort;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;

@Service
@RequiredArgsConstructor
@Slf4j
public class AlertService implements AlertUseCasePort {
    
    private final AlertRepositoryPort alertRepository;
    
    @Override
    @Transactional
    public Alert createAlert(AlertRequest request) {
        log.info("Creating alert with code: {}", request.getCode());
        
        Alert alert = Alert.builder()
                .code(request.getCode())
                .description(request.getDescription())
                .severity(request.getSeverity() != null ? request.getSeverity() : "INFO")
                .employeeId(request.getEmployeeId())
                .userId(request.getUserId())
                .additionalInfo(request.getAdditionalInfo())
                .timestamp(request.getTimestamp() != null ? request.getTimestamp() : LocalDateTime.now())
                .build();
        
        Alert savedAlert = alertRepository.save(alert);
        log.info("Alert created successfully with ID: {}", savedAlert.getId());
        
        return savedAlert;
    }
    
    @Override
    public Alert getAlertById(Long id) {
        log.info("Fetching alert by ID: {}", id);
        return alertRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Alert not found with ID: " + id));
    }
    
    @Override
    public List<Alert> getAllAlerts() {
        log.info("Fetching all alerts");
        return alertRepository.findAll();
    }
    
    @Override
    public List<Alert> getAlertsByCode(String code) {
        log.info("Fetching alerts by code: {}", code);
        return alertRepository.findByCode(code);
    }
    
    @Override
    public List<Alert> getAlertsBySeverity(String severity) {
        log.info("Fetching alerts by severity: {}", severity);
        return alertRepository.findBySeverity(severity);
    }
    
    @Override
    public List<Alert> getAlertsByEmployeeId(String employeeId) {
        log.info("Fetching alerts by employee ID: {}", employeeId);
        return alertRepository.findByEmployeeId(employeeId);
    }
    
    @Override
    public List<Alert> getAlertsByDateRange(LocalDateTime start, LocalDateTime end) {
        log.info("Fetching alerts between {} and {}", start, end);
        return alertRepository.findByTimestampBetween(start, end);
    }
    
    @Override
    public long getTotalAlerts() {
        return alertRepository.count();
    }
    
    @Override
    public long getAlertCountByCode(String code) {
        return alertRepository.countByCode(code);
    }
    
    @Override
    public long getAlertCountBySeverity(String severity) {
        return alertRepository.countBySeverity(severity);
    }
}
