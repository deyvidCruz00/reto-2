package com.uptc.alertservice.infrastructure.adapter;

import com.uptc.alertservice.domain.entity.Alert;
import com.uptc.alertservice.domain.port.AlertRepositoryPort;
import com.uptc.alertservice.infrastructure.repository.JpaAlertRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Component
@RequiredArgsConstructor
public class AlertRepositoryAdapter implements AlertRepositoryPort {
    
    private final JpaAlertRepository jpaAlertRepository;
    
    @Override
    public Alert save(Alert alert) {
        return jpaAlertRepository.save(alert);
    }
    
    @Override
    public Optional<Alert> findById(Long id) {
        return jpaAlertRepository.findById(id);
    }
    
    @Override
    public List<Alert> findAll() {
        return jpaAlertRepository.findAll();
    }
    
    @Override
    public List<Alert> findByCode(String code) {
        return jpaAlertRepository.findByCode(code);
    }
    
    @Override
    public List<Alert> findBySeverity(String severity) {
        return jpaAlertRepository.findBySeverity(severity);
    }
    
    @Override
    public List<Alert> findByEmployeeId(String employeeId) {
        return jpaAlertRepository.findByEmployeeId(employeeId);
    }
    
    @Override
    public List<Alert> findByTimestampBetween(LocalDateTime start, LocalDateTime end) {
        return jpaAlertRepository.findByTimestampBetween(start, end);
    }
    
    @Override
    public List<Alert> findByCodeAndTimestampAfter(String code, LocalDateTime timestamp) {
        return jpaAlertRepository.findByCodeAndTimestampAfter(code, timestamp);
    }
    
    @Override
    public long count() {
        return jpaAlertRepository.count();
    }
    
    @Override
    public long countByCode(String code) {
        return jpaAlertRepository.countByCode(code);
    }
    
    @Override
    public long countBySeverity(String severity) {
        return jpaAlertRepository.countBySeverity(severity);
    }
}
