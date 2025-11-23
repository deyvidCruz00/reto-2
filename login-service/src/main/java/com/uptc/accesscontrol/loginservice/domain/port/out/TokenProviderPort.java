package com.uptc.accesscontrol.loginservice.domain.port.out;

/**
 * Port for JWT Token operations - Domain interface
 * This abstracts the token generation and validation logic
 */
public interface TokenProviderPort {
    
    /**
     * Generate JWT token for a user
     * @param userId The user identifier
     * @return Generated JWT token
     */
    String generateToken(Long userId);
    
    /**
     * Extract user ID from token
     * @param token JWT token
     * @return User identifier extracted from token
     */
    Long getUserIdFromToken(String token);
    
    /**
     * Validate if token is valid
     * @param token JWT token to validate
     * @return true if token is valid, false otherwise
     */
    boolean validateToken(String token);
}
