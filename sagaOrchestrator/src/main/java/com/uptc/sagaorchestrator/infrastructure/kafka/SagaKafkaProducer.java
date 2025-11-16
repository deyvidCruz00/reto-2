package com.uptc.sagaorchestrator.infrastructure.kafka;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.uptc.sagaorchestrator.application.dto.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

import java.util.HashMap;
import java.util.Map;

@Component
@RequiredArgsConstructor
@Slf4j
public class SagaKafkaProducer {
    
    private final KafkaTemplate<String, String> kafkaTemplate;
    private final ObjectMapper objectMapper;
    
    private static final String EMPLOYEE_VALIDATION_REQUEST_TOPIC = "employee-validation-request";
    private static final String ACCESS_CHECKIN_REQUEST_TOPIC = "access-checkin-request";
    private static final String ACCESS_CHECKOUT_REQUEST_TOPIC = "access-checkout-request";
    private static final String SAGA_COMPLETED_TOPIC = "saga-completed";
    private static final String SAGA_FAILED_TOPIC = "saga-failed";
    private static final String ALERT_TOPIC = "alerts";
    
    public void sendEmployeeValidationRequest(EmployeeValidationRequest request) {
        try {
            String message = objectMapper.writeValueAsString(request);
            kafkaTemplate.send(EMPLOYEE_VALIDATION_REQUEST_TOPIC, request.getEmployeeId(), message);
            log.info("Sent employee validation request for saga: {}", request.getSagaId());
        } catch (JsonProcessingException e) {
            log.error("Error serializing employee validation request", e);
        }
    }
    
    public void sendAccessRegistrationRequest(AccessRegistrationRequest request) {
        try {
            String message = objectMapper.writeValueAsString(request);
            String topic = request.getAction().equals("CHECK_IN") ? 
                ACCESS_CHECKIN_REQUEST_TOPIC : ACCESS_CHECKOUT_REQUEST_TOPIC;
            kafkaTemplate.send(topic, request.getEmployeeId(), message);
            log.info("Sent access registration request for saga: {}, action: {}", 
                    request.getSagaId(), request.getAction());
        } catch (JsonProcessingException e) {
            log.error("Error serializing access registration request", e);
        }
    }
    
    public void sendSagaCompleted(String sagaId, String type, String accessId) {
        try {
            Map<String, Object> event = new HashMap<>();
            event.put("sagaId", sagaId);
            event.put("type", type);
            event.put("status", "COMPLETED");
            event.put("accessId", accessId);
            event.put("timestamp", System.currentTimeMillis());
            
            String message = objectMapper.writeValueAsString(event);
            kafkaTemplate.send(SAGA_COMPLETED_TOPIC, sagaId, message);
            log.info("Sent saga completed event for saga: {}", sagaId);
        } catch (JsonProcessingException e) {
            log.error("Error serializing saga completed event", e);
        }
    }
    
    public void sendSagaFailed(String sagaId, String type, String errorMessage) {
        try {
            Map<String, Object> event = new HashMap<>();
            event.put("sagaId", sagaId);
            event.put("type", type);
            event.put("status", "FAILED");
            event.put("errorMessage", errorMessage);
            event.put("timestamp", System.currentTimeMillis());
            
            String message = objectMapper.writeValueAsString(event);
            kafkaTemplate.send(SAGA_FAILED_TOPIC, sagaId, message);
            log.info("Sent saga failed event for saga: {}", sagaId);
        } catch (JsonProcessingException e) {
            log.error("Error serializing saga failed event", e);
        }
    }
    
    public void sendAlert(String employeeId, String alertType, String message) {
        try {
            Map<String, Object> alert = new HashMap<>();
            alert.put("employeeId", employeeId);
            alert.put("type", alertType);
            alert.put("message", message);
            alert.put("severity", "WARNING");
            alert.put("timestamp", System.currentTimeMillis());
            
            String alertMessage = objectMapper.writeValueAsString(alert);
            kafkaTemplate.send(ALERT_TOPIC, employeeId, alertMessage);
            log.info("Sent alert for employee: {}, type: {}", employeeId, alertType);
        } catch (JsonProcessingException e) {
            log.error("Error serializing alert", e);
        }
    }
}
