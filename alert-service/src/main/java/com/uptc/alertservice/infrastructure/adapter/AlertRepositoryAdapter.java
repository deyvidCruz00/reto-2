package com.uptc.alertservice.infrastructure.adapter;

import com.uptc.alertservice.domain.entity.AlertDomain;
import com.uptc.alertservice.domain.port.AlertRepositoryPort;
import com.uptc.alertservice.infrastructure.persistence.AlertMapper;
import com.uptc.alertservice.infrastructure.repository.JpaAlertRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Component
@RequiredArgsConstructor
public class AlertRepositoryAdapter implements AlertRepositoryPort {
    
    private final JpaAlertRepository jpaAlertRepository;
    private final AlertMapper alertMapper;
    
    @Override
    public AlertDomain save(AlertDomain alert) {
        var jpaEntity = alertMapper.toJpaEntity(alert);
        var saved = jpaAlertRepository.save(jpaEntity);
        return alertMapper.toDomain(saved);
    }
    
    @Override
    public Optional<AlertDomain> findById(Long id) {
        return jpaAlertRepository.findById(id)
                .map(alertMapper::toDomain);
    }
    
    @Override
    public List<AlertDomain> findAll() {
        return jpaAlertRepository.findAll().stream()
                .map(alertMapper::toDomain)
                .collect(Collectors.toList());
    }
    
    @Override
    public List<AlertDomain> findByCode(String code) {
        return jpaAlertRepository.findByCode(code).stream()
                .map(alertMapper::toDomain)
                .collect(Collectors.toList());
    }
    
    @Override
    public List<AlertDomain> findBySeverity(String severity) {
        return jpaAlertRepository.findBySeverity(severity).stream()
                .map(alertMapper::toDomain)
                .collect(Collectors.toList());
    }
    
    @Override
    public List<AlertDomain> findByEmployeeId(String employeeId) {
        return jpaAlertRepository.findByEmployeeId(employeeId).stream()
                .map(alertMapper::toDomain)
                .collect(Collectors.toList());
    }
    
    @Override
    public List<AlertDomain> findByTimestampBetween(LocalDateTime start, LocalDateTime end) {
        return jpaAlertRepository.findByTimestampBetween(start, end).stream()
                .map(alertMapper::toDomain)
                .collect(Collectors.toList());
    }
    
    @Override
    public List<AlertDomain> findByCodeAndTimestampAfter(String code, LocalDateTime timestamp) {
        return jpaAlertRepository.findByCodeAndTimestampAfter(code, timestamp).stream()
                .map(alertMapper::toDomain)
                .collect(Collectors.toList());
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
