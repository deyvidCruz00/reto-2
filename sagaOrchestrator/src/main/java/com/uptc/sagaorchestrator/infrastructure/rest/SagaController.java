package com.uptc.sagaorchestrator.infrastructure.rest;

import com.uptc.sagaorchestrator.application.dto.CheckInRequest;
import com.uptc.sagaorchestrator.application.dto.CheckOutRequest;
import com.uptc.sagaorchestrator.application.dto.SagaResponse;
import com.uptc.sagaorchestrator.application.service.CheckInSagaService;
import com.uptc.sagaorchestrator.application.service.CheckOutSagaService;
import com.uptc.sagaorchestrator.domain.entity.Saga;
import com.uptc.sagaorchestrator.domain.port.SagaRepositoryPort;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/saga")
@RequiredArgsConstructor
@Slf4j
public class SagaController {
    
    private final CheckInSagaService checkInSagaService;
    private final CheckOutSagaService checkOutSagaService;
    private final SagaRepositoryPort sagaRepository;
    
    @PostMapping("/check-in")
    public ResponseEntity<SagaResponse> startCheckIn(@RequestBody CheckInRequest request) {
        log.info("Starting check-in saga for employee: {}", request.getEmployeeId());
        
        try {
            Saga saga = checkInSagaService.startCheckInSaga(request.getEmployeeId());
            return ResponseEntity.status(HttpStatus.CREATED).body(toResponse(saga));
        } catch (Exception e) {
            log.error("Error starting check-in saga", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    @PostMapping("/check-out")
    public ResponseEntity<SagaResponse> startCheckOut(@RequestBody CheckOutRequest request) {
        log.info("Starting check-out saga for employee: {}", request.getEmployeeId());
        
        try {
            Saga saga = checkOutSagaService.startCheckOutSaga(request.getEmployeeId());
            return ResponseEntity.status(HttpStatus.CREATED).body(toResponse(saga));
        } catch (Exception e) {
            log.error("Error starting check-out saga", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    @GetMapping("/{sagaId}")
    public ResponseEntity<SagaResponse> getSagaStatus(@PathVariable String sagaId) {
        log.info("Getting saga status: {}", sagaId);
        
        try {
            Saga saga = checkInSagaService.getSagaStatus(sagaId);
            return ResponseEntity.ok(toResponse(saga));
        } catch (RuntimeException e) {
            log.error("Saga not found: {}", sagaId);
            return ResponseEntity.notFound().build();
        }
    }
    
    @GetMapping("/employee/{employeeId}")
    public ResponseEntity<List<SagaResponse>> getSagasByEmployee(@PathVariable String employeeId) {
        log.info("Getting sagas for employee: {}", employeeId);
        
        List<Saga> sagas = sagaRepository.findByEmployeeId(employeeId);
        List<SagaResponse> responses = sagas.stream()
                .map(this::toResponse)
                .collect(Collectors.toList());
        
        return ResponseEntity.ok(responses);
    }
    
    @GetMapping("/all")
    public ResponseEntity<List<SagaResponse>> getAllSagas() {
        log.info("Getting all sagas");
        
        List<Saga> sagas = sagaRepository.findAll();
        List<SagaResponse> responses = sagas.stream()
                .map(this::toResponse)
                .collect(Collectors.toList());
        
        return ResponseEntity.ok(responses);
    }
    
    @PostMapping("/{sagaId}/compensate")
    public ResponseEntity<Void> compensateSaga(@PathVariable String sagaId) {
        log.info("Compensating saga: {}", sagaId);
        
        try {
            checkInSagaService.compensateSaga(sagaId);
            return ResponseEntity.ok().build();
        } catch (Exception e) {
            log.error("Error compensating saga", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    @GetMapping("/health")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok("Saga Orchestrator is running");
    }
    
    private SagaResponse toResponse(Saga saga) {
        return SagaResponse.builder()
                .sagaId(saga.getId())
                .type(saga.getType().name())
                .status(saga.getStatus().name())
                .employeeId(saga.getEmployeeId())
                .employeeName(saga.getEmployeeName())
                .accessId(saga.getAccessId())
                .errorMessage(saga.getErrorMessage())
                .createdAt(saga.getCreatedAt())
                .completedAt(saga.getCompletedAt())
                .build();
    }
}
