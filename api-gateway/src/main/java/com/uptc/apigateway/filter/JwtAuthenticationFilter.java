package com.uptc.apigateway.filter;

import com.uptc.apigateway.security.JwtTokenValidator;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cloud.gateway.filter.GatewayFilter;
import org.springframework.cloud.gateway.filter.factory.AbstractGatewayFilterFactory;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.server.reactive.ServerHttpRequest;
import org.springframework.http.server.reactive.ServerHttpResponse;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;

/**
 * JWT Authentication Filter for API Gateway
 * Validates JWT tokens for protected routes
 */
@Component
@Slf4j
public class JwtAuthenticationFilter extends AbstractGatewayFilterFactory<JwtAuthenticationFilter.Config> {
    
    @Autowired
    private JwtTokenValidator jwtTokenValidator;
    
    public JwtAuthenticationFilter() {
        super(Config.class);
    }
    
    @Override
    public GatewayFilter apply(Config config) {
        return (exchange, chain) -> {
            ServerHttpRequest request = exchange.getRequest();
            
            // Skip authentication for public paths
            if (isPublicPath(request.getPath().toString())) {
                return chain.filter(exchange);
            }
            
            // Extract Authorization header
            if (!request.getHeaders().containsKey(HttpHeaders.AUTHORIZATION)) {
                log.warn("Missing Authorization header for path: {}", request.getPath());
                return onError(exchange, "Missing Authorization header", HttpStatus.UNAUTHORIZED);
            }
            
            String authHeader = request.getHeaders().getFirst(HttpHeaders.AUTHORIZATION);
            
            if (authHeader == null || !authHeader.startsWith("Bearer ")) {
                log.warn("Invalid Authorization header format");
                return onError(exchange, "Invalid Authorization header format", HttpStatus.UNAUTHORIZED);
            }
            
            String token = authHeader.substring(7);
            
            // Validate token
            if (!jwtTokenValidator.validateToken(token)) {
                log.warn("Invalid or expired JWT token");
                return onError(exchange, "Invalid or expired token", HttpStatus.FORBIDDEN);
            }
            
            // Extract user ID and add to headers
            String userId = jwtTokenValidator.getUserIdFromToken(token);
            if (userId != null) {
                ServerHttpRequest modifiedRequest = exchange.getRequest()
                        .mutate()
                        .header("X-User-Id", userId)
                        .build();
                
                exchange = exchange.mutate().request(modifiedRequest).build();
            }
            
            log.debug("JWT validated successfully for user: {}", userId);
            return chain.filter(exchange);
        };
    }
    
    private boolean isPublicPath(String path) {
        return path.startsWith("/login") ||
               path.startsWith("/actuator") ||
               path.startsWith("/health") ||
               path.startsWith("/metrics");
    }
    
    private Mono<Void> onError(ServerWebExchange exchange, String error, HttpStatus httpStatus) {
        ServerHttpResponse response = exchange.getResponse();
        response.setStatusCode(httpStatus);
        return response.setComplete();
    }
    
    public static class Config {
        // Configuration properties if needed
    }
}
