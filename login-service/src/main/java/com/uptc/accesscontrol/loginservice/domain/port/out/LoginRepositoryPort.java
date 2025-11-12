package com.uptc.accesscontrol.loginservice.domain.port.out;

import com.uptc.accesscontrol.loginservice.domain.model.Login;

import java.util.Optional;

public interface LoginRepositoryPort {
    
    Login save(Login login);
    
    Optional<Login> findByUserId(Long userId);
    
    boolean existsByUserId(Long userId);
    
    void updateFailedAttempts(Long userId, int attempts);
    
    void lockUser(Long userId);
    
    void unlockUser(Long userId);
}
