package com.uptc.alertservice.application.service;

import com.uptc.alertservice.application.dto.AlertRequest;
import com.uptc.alertservice.domain.entity.AlertDomain;
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
    public AlertDomain createAlert(AlertRequest request) {
        log.info("Creating alert with code: {}", request.getCode());
        
        AlertDomain alert = new AlertDomain(
                null,
                request.getTimestamp() != null ? request.getTimestamp() : LocalDateTime.now(),
                request.getDescription(),
                request.getCode(),
                request.getSeverity() != null ? request.getSeverity() : "INFO",
                request.getEmployeeId(),
                request.getUserId(),
                request.getAdditionalInfo()
        );
        
        AlertDomain savedAlert = alertRepository.save(alert);
        log.info("Alert created successfully with ID: {}", savedAlert.getId());
        
        return savedAlert;
    }
    
    @Override
    public AlertDomain getAlertById(Long id) {
        log.info("Fetching alert by ID: {}", id);
        return alertRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Alert not found with ID: " + id));
    }
    
    @Override
    public List<AlertDomain> getAllAlerts() {
        log.info("Fetching all alerts");
        return alertRepository.findAll();
    }
    
    @Override
    public List<AlertDomain> getAlertsByCode(String code) {
        log.info("Fetching alerts by code: {}", code);
        return alertRepository.findByCode(code);
    }
    
    @Override
    public List<AlertDomain> getAlertsBySeverity(String severity) {
        log.info("Fetching alerts by severity: {}", severity);
        return alertRepository.findBySeverity(severity);
    }
    
    @Override
    public List<AlertDomain> getAlertsByEmployeeId(String employeeId) {
        log.info("Fetching alerts by employee ID: {}", employeeId);
        return alertRepository.findByEmployeeId(employeeId);
    }
    
    @Override
    public List<AlertDomain> getAlertsByDateRange(LocalDateTime start, LocalDateTime end) {
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
