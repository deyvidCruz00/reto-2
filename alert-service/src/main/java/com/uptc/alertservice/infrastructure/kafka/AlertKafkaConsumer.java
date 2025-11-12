package com.uptc.alertservice.infrastructure.kafka;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.uptc.alertservice.application.dto.AlertRequest;
import com.uptc.alertservice.domain.port.AlertUseCasePort;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

@Component
@RequiredArgsConstructor
@Slf4j
public class AlertKafkaConsumer {
    
    private final AlertUseCasePort alertUseCase;
    private final ObjectMapper objectMapper;
    
    @KafkaListener(topics = "${kafka.topic.alert-notification}", groupId = "${spring.kafka.consumer.group-id}")
    public void consumeAlertNotification(String message) {
        try {
            log.info("Received alert notification: {}", message);
            
            JsonNode jsonNode = objectMapper.readTree(message);
            
            // Extract alert information
            String code = getStringValue(jsonNode, "code");
            String description = getStringValue(jsonNode, "description");
            String severity = getStringValue(jsonNode, "severity", "WARNING");
            String employeeId = getStringValue(jsonNode, "employee_id");
            String userId = getStringValue(jsonNode, "userId");
            
            // Create alert request
            AlertRequest alertRequest = AlertRequest.builder()
                    .code(code)
                    .description(description)
                    .severity(severity)
                    .employeeId(employeeId)
                    .userId(userId)
                    .timestamp(LocalDateTime.now())
                    .additionalInfo(message)
                    .build();
            
            // Save alert
            alertUseCase.createAlert(alertRequest);
            log.info("Alert saved successfully: {}", code);
            
        } catch (JsonProcessingException e) {
            log.error("Error parsing JSON message: {}", message, e);
        } catch (Exception e) {
            log.error("Error processing alert notification", e);
        }
    }
    
    private String getStringValue(JsonNode node, String fieldName) {
        return getStringValue(node, fieldName, null);
    }
    
    private String getStringValue(JsonNode node, String fieldName, String defaultValue) {
        JsonNode fieldNode = node.get(fieldName);
        if (fieldNode != null && !fieldNode.isNull()) {
            return fieldNode.asText();
        }
        return defaultValue;
    }
}
