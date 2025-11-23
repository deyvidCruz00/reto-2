package com.uptc.alertservice.domain.port;

import com.uptc.alertservice.application.dto.AlertRequest;
import com.uptc.alertservice.domain.entity.AlertDomain;

import java.time.LocalDateTime;
import java.util.List;

public interface AlertUseCasePort {
    AlertDomain createAlert(AlertRequest request);
    AlertDomain getAlertById(Long id);
    List<AlertDomain> getAllAlerts();
    List<AlertDomain> getAlertsByCode(String code);
    List<AlertDomain> getAlertsBySeverity(String severity);
    List<AlertDomain> getAlertsByEmployeeId(String employeeId);
    List<AlertDomain> getAlertsByDateRange(LocalDateTime start, LocalDateTime end);
    long getTotalAlerts();
    long getAlertCountByCode(String code);
    long getAlertCountBySeverity(String severity);
}
