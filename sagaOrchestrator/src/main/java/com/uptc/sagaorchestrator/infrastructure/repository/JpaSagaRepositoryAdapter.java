package com.uptc.sagaorchestrator.infrastructure.repository;

import com.uptc.sagaorchestrator.domain.entity.Saga;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface JpaSagaRepositoryAdapter extends JpaRepository<Saga, String> {
    
    List<Saga> findByEmployeeId(String employeeId);
    
    List<Saga> findByStatus(Saga.SagaStatus status);
    
    @Query("SELECT s FROM Saga s WHERE s.employeeId = :employeeId " +
           "AND s.type = 'CHECK_IN' " +
           "AND s.status NOT IN ('COMPLETED', 'FAILED', 'COMPENSATED')")
    Optional<Saga> findActiveCheckInByEmployeeId(@Param("employeeId") String employeeId);
    
    @Query("SELECT s FROM Saga s WHERE s.createdAt < :timeout " +
           "AND s.status NOT IN ('COMPLETED', 'FAILED', 'COMPENSATED')")
    List<Saga> findTimedOutSagas(@Param("timeout") LocalDateTime timeout);
}
