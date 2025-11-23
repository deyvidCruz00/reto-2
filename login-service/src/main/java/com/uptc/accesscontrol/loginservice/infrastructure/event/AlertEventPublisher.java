package com.uptc.accesscontrol.loginservice.infrastructure.event;

import com.uptc.accesscontrol.loginservice.domain.port.out.AlertEventPublisherPort;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.util.UUID;

/**
 * Kafka Alert Event Publisher Adapter - Infrastructure implementation
 * Implements the AlertEventPublisherPort using Kafka
 */
@Component
@RequiredArgsConstructor
@Slf4j
public class AlertEventPublisher implements AlertEventPublisherPort {

    private final KafkaTemplate<String, AlertEvent> kafkaTemplate;
    private static final String ALERT_TOPIC = "alert-notification";

    @Override
    public void publishUserNotRegisteredAlert(Long userId) {
        AlertEvent event = AlertEvent.builder()
                .alertId(UUID.randomUUID().toString())
                .timestamp(LocalDateTime.now())
                .description("User not registered attempted to login")
                .code("LOGIN_USR_NOT_REGISTERED")
                .userId(userId)
                .severity("MEDIUM")
                .build();

        kafkaTemplate.send(ALERT_TOPIC, event);
        log.info("Published alert for non-registered user: {}", userId);
    }

    @Override
    public void publishUserExceededAttemptsAlert(Long userId) {
        AlertEvent event = AlertEvent.builder()
                .alertId(UUID.randomUUID().toString())
                .timestamp(LocalDateTime.now())
                .description("User exceeded maximum login attempts")
                .code("LOGIN_USR_ATTEMPS_EXCEEDED")
                .userId(userId)
                .severity("HIGH")
                .build();

        kafkaTemplate.send(ALERT_TOPIC, event);
        log.info("Published alert for exceeded attempts: {}", userId);
    }
}
