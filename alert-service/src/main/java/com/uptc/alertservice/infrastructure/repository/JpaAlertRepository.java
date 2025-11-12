package com.uptc.alertservice.infrastructure.repository;

import com.uptc.alertservice.domain.entity.Alert;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface JpaAlertRepository extends JpaRepository<Alert, Long> {
    List<Alert> findByCode(String code);
    List<Alert> findBySeverity(String severity);
    List<Alert> findByEmployeeId(String employeeId);
    List<Alert> findByTimestampBetween(LocalDateTime start, LocalDateTime end);
    List<Alert> findByCodeAndTimestampAfter(String code, LocalDateTime timestamp);
    long countByCode(String code);
    long countBySeverity(String severity);
}
