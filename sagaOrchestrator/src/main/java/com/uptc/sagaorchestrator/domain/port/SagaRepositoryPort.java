package com.uptc.sagaorchestrator.domain.port;

import com.uptc.sagaorchestrator.domain.entity.Saga;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

public interface SagaRepositoryPort {
    
    Saga save(Saga saga);
    
    Saga saveAndFlush(Saga saga);
    
    Optional<Saga> findById(String id);
    
    List<Saga> findByEmployeeId(String employeeId);
    
    List<Saga> findByStatus(Saga.SagaStatus status);
    
    List<Saga> findTimedOutSagas(LocalDateTime timeout);
    
    Optional<Saga> findActiveCheckInByEmployeeId(String employeeId);
    
    void delete(Saga saga);
    
    List<Saga> findAll();
}
