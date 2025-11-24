package com.uptc.sagaorchestrator.application.service;

import com.uptc.sagaorchestrator.application.dto.*;
import com.uptc.sagaorchestrator.domain.entity.Saga;
import com.uptc.sagaorchestrator.domain.entity.SagaLog;
import com.uptc.sagaorchestrator.domain.entity.SagaStep;
import com.uptc.sagaorchestrator.domain.port.SagaRepositoryPort;
import com.uptc.sagaorchestrator.domain.port.SagaUseCasePort;
import com.uptc.sagaorchestrator.infrastructure.kafka.SagaKafkaProducer;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class CheckOutSagaService implements SagaUseCasePort {
    
    private final SagaRepositoryPort sagaRepository;
    private final SagaKafkaProducer kafkaProducer;
    
    @Override
    @Transactional
    public Saga startCheckOutSaga(String employeeId) {
        log.info("Starting CHECK_OUT saga for employee: {}", employeeId);
        
        // Crear nueva saga
        Saga saga = Saga.builder()
                .type(Saga.SagaType.CHECK_OUT)
                .status(Saga.SagaStatus.STARTED)
                .employeeId(employeeId)
                .createdAt(LocalDateTime.now())
                .build();
        
        saga = sagaRepository.saveAndFlush(saga);
        
        // Log inicial
        addLog(saga, SagaLog.LogLevel.INFO, "Saga CHECK_OUT iniciada", 
               "Saga ID: " + saga.getId() + ", Employee ID: " + employeeId);
        
        // Paso 1: Solicitar validación de empleado
        executeStep1_ValidateEmployee(saga);
        
        return sagaRepository.save(saga);
    }
    
    private void executeStep1_ValidateEmployee(Saga saga) {
        log.debug("Executing Step 1: Validate Employee for saga {}", saga.getId());
        
        SagaStep step = SagaStep.builder()
                .saga(saga)
                .stepNumber(1)
                .stepName("VALIDATE_EMPLOYEE")
                .status(SagaStep.StepStatus.IN_PROGRESS)
                .startedAt(LocalDateTime.now())
                .build();
        
        saga.addStep(step);
        saga.setStatus(Saga.SagaStatus.PENDING_EMPLOYEE_VALIDATION);
        
        addLog(saga, SagaLog.LogLevel.INFO, "Iniciando validación de empleado", 
               "Employee ID: " + saga.getEmployeeId());
        
        // CRITICAL: Save before sending Kafka message to ensure visibility
        saga = sagaRepository.saveAndFlush(saga);
        
        // Enviar mensaje Kafka para validar empleado
        EmployeeValidationRequest request = EmployeeValidationRequest.builder()
                .sagaId(saga.getId())
                .employeeId(saga.getEmployeeId())
                .action("CHECK_OUT")
                .build();
        
        kafkaProducer.sendEmployeeValidationRequest(request);
        
        addLog(saga, SagaLog.LogLevel.DEBUG, "Solicitud de validación enviada", 
               "Topic: employee-validation-request");
    }
    
    @Override
    @Transactional
    public void handleEmployeeValidationResponse(String sagaId, boolean isValid, 
                                                  String employeeName, String errorMessage) {
        log.info("Handling employee validation response for saga: {}, isValid: {}", sagaId, isValid);
        
        Optional<Saga> sagaOpt = sagaRepository.findById(sagaId);
        if (sagaOpt.isEmpty()) {
            log.error("Saga not found: {}", sagaId);
            return;
        }
        
        Saga saga = sagaOpt.get();
        
        // Encontrar el paso de validación
        Optional<SagaStep> stepOpt = saga.getSteps().stream()
                .filter(s -> s.getStepName().equals("VALIDATE_EMPLOYEE"))
                .findFirst();
        
        if (stepOpt.isEmpty()) {
            log.error("Validation step not found for saga: {}", sagaId);
            return;
        }
        
        SagaStep step = stepOpt.get();
        
        if (isValid) {
            // Validación exitosa
            step.complete("Employee validated: " + employeeName);
            saga.setEmployeeName(employeeName);
            saga.setStatus(Saga.SagaStatus.EMPLOYEE_VALIDATED);
            
            addLog(saga, SagaLog.LogLevel.INFO, "Empleado validado exitosamente", 
                   "Employee: " + employeeName);
            
            sagaRepository.save(saga);
            
            // Paso 2: Registrar salida
            executeStep2_RegisterAccess(saga);
            
        } else {
            // Validación fallida
            step.fail(errorMessage);
            saga.fail(errorMessage);
            
            addLog(saga, SagaLog.LogLevel.ERROR, "Validación de empleado fallida", errorMessage);
            
            sagaRepository.save(saga);
            
            // Publicar evento de fallo
            kafkaProducer.sendSagaFailed(sagaId, "CHECK_OUT", errorMessage);
        }
    }
    
    private void executeStep2_RegisterAccess(Saga saga) {
        log.debug("Executing Step 2: Register Access (Check-Out) for saga {}", saga.getId());
        
        SagaStep step = SagaStep.builder()
                .saga(saga)
                .stepNumber(2)
                .stepName("REGISTER_ACCESS")
                .status(SagaStep.StepStatus.IN_PROGRESS)
                .startedAt(LocalDateTime.now())
                .build();
        
        saga.addStep(step);
        saga.setStatus(Saga.SagaStatus.PENDING_ACCESS_REGISTRATION);
        
        addLog(saga, SagaLog.LogLevel.INFO, "Registrando salida de acceso", 
               "Employee: " + saga.getEmployeeName());
        
        // CRITICAL: Save before sending Kafka message to ensure visibility
        saga = sagaRepository.saveAndFlush(saga);
        
        // Enviar mensaje Kafka para registrar salida
        AccessRegistrationRequest request = AccessRegistrationRequest.builder()
                .sagaId(saga.getId())
                .employeeId(saga.getEmployeeId())
                .employeeName(saga.getEmployeeName())
                .action("CHECK_OUT")
                .build();
        
        kafkaProducer.sendAccessRegistrationRequest(request);
        
        addLog(saga, SagaLog.LogLevel.DEBUG, "Solicitud de registro enviada", 
               "Topic: access-checkout-request");
        
        sagaRepository.save(saga);
    }
    
    @Override
    @Transactional
    public void handleAccessRegistrationResponse(String sagaId, boolean isSuccess, 
                                                  String accessId, String errorMessage) {
        log.info("Handling access registration response for saga: {}, success: {}", sagaId, isSuccess);
        
        Optional<Saga> sagaOpt = sagaRepository.findById(sagaId);
        if (sagaOpt.isEmpty()) {
            log.error("Saga not found: {}", sagaId);
            return;
        }
        
        Saga saga = sagaOpt.get();
        
        // Encontrar el paso de registro
        Optional<SagaStep> stepOpt = saga.getSteps().stream()
                .filter(s -> s.getStepName().equals("REGISTER_ACCESS"))
                .findFirst();
        
        if (stepOpt.isEmpty()) {
            log.error("Register step not found for saga: {}", sagaId);
            return;
        }
        
        SagaStep step = stepOpt.get();
        
        if (isSuccess) {
            // Registro exitoso
            step.complete("Access updated: " + accessId);
            saga.setAccessId(accessId);
            saga.setStatus(Saga.SagaStatus.ACCESS_REGISTERED);
            saga.complete();
            
            addLog(saga, SagaLog.LogLevel.INFO, "Salida registrada exitosamente", 
                   "Access ID: " + accessId);
            
            sagaRepository.save(saga);
            
            // Publicar evento de éxito
            kafkaProducer.sendSagaCompleted(sagaId, "CHECK_OUT", accessId);
            
        } else {
            // Registro fallido
            step.fail(errorMessage);
            saga.fail(errorMessage);
            
            addLog(saga, SagaLog.LogLevel.ERROR, "Registro de salida fallido", errorMessage);
            
            sagaRepository.save(saga);
            
            // Publicar evento de fallo
            kafkaProducer.sendSagaFailed(sagaId, "CHECK_OUT", errorMessage);
        }
    }
    
    @Override
    @Transactional
    public void handleSagaTimeout(String sagaId) {
        log.warn("Handling saga timeout for: {}", sagaId);
        
        Optional<Saga> sagaOpt = sagaRepository.findById(sagaId);
        if (sagaOpt.isEmpty()) {
            log.error("Saga not found: {}", sagaId);
            return;
        }
        
        Saga saga = sagaOpt.get();
        
        if (saga.getStatus() == Saga.SagaStatus.COMPLETED || 
            saga.getStatus() == Saga.SagaStatus.FAILED) {
            return; // Ya está completada o fallida
        }
        
        addLog(saga, SagaLog.LogLevel.ERROR, "Saga timeout", 
               "Saga excedió el tiempo límite de 30 segundos");
        
        saga.fail("Saga timeout after 30 seconds");
        sagaRepository.save(saga);
        
        kafkaProducer.sendSagaFailed(sagaId, saga.getType().name(), "Timeout");
    }
    
    @Override
    public Saga getSagaStatus(String sagaId) {
        return sagaRepository.findById(sagaId)
                .orElseThrow(() -> new RuntimeException("Saga not found: " + sagaId));
    }
    
    @Override
    @Transactional
    public void compensateSaga(String sagaId) {
        log.info("Compensating saga: {}", sagaId);
        
        Optional<Saga> sagaOpt = sagaRepository.findById(sagaId);
        if (sagaOpt.isEmpty()) {
            log.error("Saga not found: {}", sagaId);
            return;
        }
        
        Saga saga = sagaOpt.get();
        saga.compensate();
        
        addLog(saga, SagaLog.LogLevel.INFO, "Iniciando compensación", 
               "Revirtiendo pasos completados");
        
        // Compensar pasos en orden inverso
        saga.getSteps().stream()
                .filter(s -> s.getStatus() == SagaStep.StepStatus.COMPLETED)
                .sorted((a, b) -> b.getStepNumber().compareTo(a.getStepNumber()))
                .forEach(step -> {
                    step.compensate();
                    addLog(saga, SagaLog.LogLevel.INFO, "Paso compensado", 
                           "Step: " + step.getStepName());
                });
        
        saga.compensated();
        sagaRepository.save(saga);
        
        addLog(saga, SagaLog.LogLevel.INFO, "Compensación completada", "Saga compensada");
    }
    
    @Override
    public Saga startCheckInSaga(String employeeId) {
        throw new UnsupportedOperationException("Use CheckInSagaService for check-in operations");
    }
    
    private void addLog(Saga saga, SagaLog.LogLevel level, String message, String details) {
        SagaLog log = SagaLog.builder()
                .saga(saga)
                .level(level)
                .message(message)
                .details(details)
                .timestamp(LocalDateTime.now())
                .build();
        
        saga.addLog(log);
    }
}
