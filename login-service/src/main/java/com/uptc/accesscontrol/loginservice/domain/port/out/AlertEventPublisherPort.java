package com.uptc.accesscontrol.loginservice.domain.port.out;

/**
 * Port for publishing alert events - Domain interface
 * This abstracts the event publishing mechanism
 */
public interface AlertEventPublisherPort {
    
    /**
     * Publish alert when user is not registered
     * @param userId The user identifier attempting to authenticate
     */
    void publishUserNotRegisteredAlert(Long userId);
    
    /**
     * Publish alert when user exceeds login attempts
     * @param userId The user identifier who exceeded attempts
     */
    void publishUserExceededAttemptsAlert(Long userId);
}
