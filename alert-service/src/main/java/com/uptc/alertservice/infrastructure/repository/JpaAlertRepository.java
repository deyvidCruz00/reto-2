package com.uptc.alertservice.infrastructure.repository;

import com.uptc.alertservice.infrastructure.persistence.AlertJpaEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface JpaAlertRepository extends JpaRepository<AlertJpaEntity, Long> {
    List<AlertJpaEntity> findByCode(String code);
    List<AlertJpaEntity> findBySeverity(String severity);
    List<AlertJpaEntity> findByEmployeeId(String employeeId);
    List<AlertJpaEntity> findByTimestampBetween(LocalDateTime start, LocalDateTime end);
    List<AlertJpaEntity> findByCodeAndTimestampAfter(String code, LocalDateTime timestamp);
    long countByCode(String code);
    long countBySeverity(String severity);
}
