package com.uptc.sagaorchestrator.domain.port;

import com.uptc.sagaorchestrator.domain.entity.Saga;

public interface SagaUseCasePort {
    
    /**
     * Inicia una saga de check-in
     */
    Saga startCheckInSaga(String employeeId);
    
    /**
     * Inicia una saga de check-out
     */
    Saga startCheckOutSaga(String employeeId);
    
    /**
     * Procesa respuesta de validación de empleado
     */
    void handleEmployeeValidationResponse(String sagaId, boolean isValid, String employeeName, String errorMessage);
    
    /**
     * Procesa respuesta de registro de acceso
     */
    void handleAccessRegistrationResponse(String sagaId, boolean isSuccess, String accessId, String errorMessage);
    
    /**
     * Maneja el timeout de una saga
     */
    void handleSagaTimeout(String sagaId);
    
    /**
     * Obtiene el estado de una saga
     */
    Saga getSagaStatus(String sagaId);
    
    /**
     * Compensa una saga fallida
     */
    void compensateSaga(String sagaId);
}
