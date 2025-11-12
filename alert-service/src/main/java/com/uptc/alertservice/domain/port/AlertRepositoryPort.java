package com.uptc.alertservice.domain.port;

import com.uptc.alertservice.domain.entity.Alert;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

public interface AlertRepositoryPort {
    Alert save(Alert alert);
    Optional<Alert> findById(Long id);
    List<Alert> findAll();
    List<Alert> findByCode(String code);
    List<Alert> findBySeverity(String severity);
    List<Alert> findByEmployeeId(String employeeId);
    List<Alert> findByTimestampBetween(LocalDateTime start, LocalDateTime end);
    List<Alert> findByCodeAndTimestampAfter(String code, LocalDateTime timestamp);
    long count();
    long countByCode(String code);
    long countBySeverity(String severity);
}
