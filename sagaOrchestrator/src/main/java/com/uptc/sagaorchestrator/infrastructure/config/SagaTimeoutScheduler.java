package com.uptc.sagaorchestrator.infrastructure.config;

import com.uptc.sagaorchestrator.application.service.CheckInSagaService;
import com.uptc.sagaorchestrator.application.service.CheckOutSagaService;
import com.uptc.sagaorchestrator.domain.entity.Saga;
import com.uptc.sagaorchestrator.domain.port.SagaRepositoryPort;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.util.List;

@Component
@RequiredArgsConstructor
@Slf4j
public class SagaTimeoutScheduler {
    
    private final SagaRepositoryPort sagaRepository;
    private final CheckInSagaService checkInSagaService;
    private final CheckOutSagaService checkOutSagaService;
    
    @Value("${saga.timeout.seconds:30}")
    private int timeoutSeconds;
    
    @Scheduled(fixedDelay = 5000) // Check every 5 seconds
    public void checkTimedOutSagas() {
        LocalDateTime timeoutThreshold = LocalDateTime.now().minusSeconds(timeoutSeconds);
        
        List<Saga> timedOutSagas = sagaRepository.findTimedOutSagas(timeoutThreshold);
        
        if (!timedOutSagas.isEmpty()) {
            log.info("Found {} timed out sagas", timedOutSagas.size());
            
            for (Saga saga : timedOutSagas) {
                log.warn("Processing timeout for saga: {}", saga.getId());
                
                if (saga.getType() == Saga.SagaType.CHECK_IN) {
                    checkInSagaService.handleSagaTimeout(saga.getId());
                } else if (saga.getType() == Saga.SagaType.CHECK_OUT) {
                    checkOutSagaService.handleSagaTimeout(saga.getId());
                }
            }
        }
    }
}
