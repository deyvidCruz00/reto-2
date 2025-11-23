package com.uptc.apigateway.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Mono;

import java.util.HashMap;
import java.util.Map;

/**
 * Fallback Controller for Circuit Breaker
 * Provides fallback responses when services are unavailable
 */
@RestController
@RequestMapping("/fallback")
public class FallbackController {
    
    @GetMapping("/employee")
    public Mono<ResponseEntity<Map<String, Object>>> employeeFallback() {
        return Mono.just(createFallbackResponse("Employee Service is temporarily unavailable"));
    }
    
    @GetMapping("/access")
    public Mono<ResponseEntity<Map<String, Object>>> accessFallback() {
        return Mono.just(createFallbackResponse("Access Control Service is temporarily unavailable"));
    }
    
    @GetMapping("/alert")
    public Mono<ResponseEntity<Map<String, Object>>> alertFallback() {
        return Mono.just(createFallbackResponse("Alert Service is temporarily unavailable"));
    }
    
    @GetMapping("/saga")
    public Mono<ResponseEntity<Map<String, Object>>> sagaFallback() {
        return Mono.just(createFallbackResponse("SAGA Orchestrator is temporarily unavailable"));
    }
    
    private ResponseEntity<Map<String, Object>> createFallbackResponse(String message) {
        Map<String, Object> response = new HashMap<>();
        response.put("error", true);
        response.put("message", message);
        response.put("status", HttpStatus.SERVICE_UNAVAILABLE.value());
        
        return ResponseEntity
                .status(HttpStatus.SERVICE_UNAVAILABLE)
                .body(response);
    }
}
