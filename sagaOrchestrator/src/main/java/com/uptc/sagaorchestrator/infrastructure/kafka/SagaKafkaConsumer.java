package com.uptc.sagaorchestrator.infrastructure.kafka;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.uptc.sagaorchestrator.application.dto.AccessRegistrationResponse;
import com.uptc.sagaorchestrator.application.dto.EmployeeValidationResponse;
import com.uptc.sagaorchestrator.application.service.CheckInSagaService;
import com.uptc.sagaorchestrator.application.service.CheckOutSagaService;
import com.uptc.sagaorchestrator.domain.entity.Saga;
import com.uptc.sagaorchestrator.domain.port.SagaRepositoryPort;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.support.Acknowledgment;
import org.springframework.stereotype.Component;

import java.util.Optional;

@Component
@RequiredArgsConstructor
@Slf4j
public class SagaKafkaConsumer {
    
    private final CheckInSagaService checkInSagaService;
    private final CheckOutSagaService checkOutSagaService;
    private final SagaRepositoryPort sagaRepository;
    private final ObjectMapper objectMapper;
    
    @KafkaListener(topics = "employee-validation-response", groupId = "saga-orchestrator-group")
    public void consumeEmployeeValidationResponse(String message, Acknowledgment ack) {
        try {
            log.info("Received employee validation response: {}", message);
            
            EmployeeValidationResponse response = objectMapper.readValue(message, 
                EmployeeValidationResponse.class);
            
            // Determinar el tipo de saga y delegar al servicio correspondiente
            Optional<Saga> sagaOpt = sagaRepository.findById(response.getSagaId());
            if (sagaOpt.isPresent()) {
                Saga saga = sagaOpt.get();
                
                if (saga.getType() == Saga.SagaType.CHECK_IN) {
                    checkInSagaService.handleEmployeeValidationResponse(
                        response.getSagaId(),
                        response.getIsValid(),
                        response.getEmployeeName(),
                        response.getErrorMessage()
                    );
                } else if (saga.getType() == Saga.SagaType.CHECK_OUT) {
                    checkOutSagaService.handleEmployeeValidationResponse(
                        response.getSagaId(),
                        response.getIsValid(),
                        response.getEmployeeName(),
                        response.getErrorMessage()
                    );
                }
            } else {
                log.error("Saga not found: {}", response.getSagaId());
            }
            
            ack.acknowledge();
        } catch (Exception e) {
            log.error("Error processing employee validation response", e);
        }
    }
    
    @KafkaListener(topics = "access-checkin-response", groupId = "saga-orchestrator-group")
    public void consumeAccessCheckInResponse(String message, Acknowledgment ack) {
        try {
            log.info("Received access check-in response: {}", message);
            
            AccessRegistrationResponse response = objectMapper.readValue(message, 
                AccessRegistrationResponse.class);
            
            checkInSagaService.handleAccessRegistrationResponse(
                response.getSagaId(),
                response.getSuccess(),
                response.getAccessId(),
                response.getErrorMessage()
            );
            
            ack.acknowledge();
        } catch (Exception e) {
            log.error("Error processing access check-in response", e);
        }
    }
    
    @KafkaListener(topics = "access-checkout-response", groupId = "saga-orchestrator-group")
    public void consumeAccessCheckOutResponse(String message, Acknowledgment ack) {
        try {
            log.info("Received access check-out response: {}", message);
            
            AccessRegistrationResponse response = objectMapper.readValue(message, 
                AccessRegistrationResponse.class);
            
            checkOutSagaService.handleAccessRegistrationResponse(
                response.getSagaId(),
                response.getSuccess(),
                response.getAccessId(),
                response.getErrorMessage()
            );
            
            ack.acknowledge();
        } catch (Exception e) {
            log.error("Error processing access check-out response", e);
        }
    }
}
