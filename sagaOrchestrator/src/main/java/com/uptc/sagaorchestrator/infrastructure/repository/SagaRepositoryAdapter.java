package com.uptc.sagaorchestrator.infrastructure.repository;

import com.uptc.sagaorchestrator.domain.entity.Saga;
import com.uptc.sagaorchestrator.domain.port.SagaRepositoryPort;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Component
@RequiredArgsConstructor
public class SagaRepositoryAdapter implements SagaRepositoryPort {
    
    private final JpaSagaRepositoryAdapter jpaRepository;
    
    @Override
    public Saga save(Saga saga) {
        return jpaRepository.save(saga);
    }
    
    @Override
    public Saga saveAndFlush(Saga saga) {
        return jpaRepository.saveAndFlush(saga);
    }
    
    @Override
    public Optional<Saga> findById(String id) {
        return jpaRepository.findById(id);
    }
    
    @Override
    public List<Saga> findByEmployeeId(String employeeId) {
        return jpaRepository.findByEmployeeId(employeeId);
    }
    
    @Override
    public List<Saga> findByStatus(Saga.SagaStatus status) {
        return jpaRepository.findByStatus(status);
    }
    
    @Override
    public List<Saga> findTimedOutSagas(LocalDateTime timeout) {
        return jpaRepository.findTimedOutSagas(timeout);
    }
    
    @Override
    public Optional<Saga> findActiveCheckInByEmployeeId(String employeeId) {
        return jpaRepository.findActiveCheckInByEmployeeId(employeeId);
    }
    
    @Override
    public void delete(Saga saga) {
        jpaRepository.delete(saga);
    }
    
    @Override
    public List<Saga> findAll() {
        return jpaRepository.findAll();
    }
}
