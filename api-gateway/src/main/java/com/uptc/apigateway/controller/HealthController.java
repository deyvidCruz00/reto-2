package com.uptc.apigateway.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Mono;

import java.util.HashMap;
import java.util.Map;

/**
 * Health Check Controller
 */
@RestController
public class HealthController {
    
    @GetMapping("/health")
    public Mono<ResponseEntity<Map<String, String>>> health() {
        Map<String, String> response = new HashMap<>();
        response.put("status", "UP");
        response.put("service", "API Gateway");
        response.put("version", "1.0.0");
        
        return Mono.just(ResponseEntity.ok(response));
    }
}
