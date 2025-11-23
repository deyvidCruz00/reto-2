package com.uptc.alertservice.domain.port;

import com.uptc.alertservice.domain.entity.AlertDomain;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

public interface AlertRepositoryPort {
    AlertDomain save(AlertDomain alert);
    Optional<AlertDomain> findById(Long id);
    List<AlertDomain> findAll();
    List<AlertDomain> findByCode(String code);
    List<AlertDomain> findBySeverity(String severity);
    List<AlertDomain> findByEmployeeId(String employeeId);
    List<AlertDomain> findByTimestampBetween(LocalDateTime start, LocalDateTime end);
    List<AlertDomain> findByCodeAndTimestampAfter(String code, LocalDateTime timestamp);
    long count();
    long countByCode(String code);
    long countBySeverity(String severity);
}
