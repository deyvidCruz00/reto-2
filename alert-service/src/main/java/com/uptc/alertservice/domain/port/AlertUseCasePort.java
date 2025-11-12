package com.uptc.alertservice.domain.port;

import com.uptc.alertservice.application.dto.AlertRequest;
import com.uptc.alertservice.domain.entity.Alert;

import java.time.LocalDateTime;
import java.util.List;

public interface AlertUseCasePort {
    Alert createAlert(AlertRequest request);
    Alert getAlertById(Long id);
    List<Alert> getAllAlerts();
    List<Alert> getAlertsByCode(String code);
    List<Alert> getAlertsBySeverity(String severity);
    List<Alert> getAlertsByEmployeeId(String employeeId);
    List<Alert> getAlertsByDateRange(LocalDateTime start, LocalDateTime end);
    long getTotalAlerts();
    long getAlertCountByCode(String code);
    long getAlertCountBySeverity(String severity);
}
