package com.uptc.accesscontrol.loginservice.domain.port.out;

import com.uptc.accesscontrol.loginservice.domain.model.LoginDomain;

import java.util.Optional;

public interface LoginRepositoryPort {
    
    LoginDomain save(LoginDomain login);
    
    Optional<LoginDomain> findByUserId(Long userId);
    
    boolean existsByUserId(Long userId);
    
    void updateFailedAttempts(Long userId, int attempts);
    
    void lockUser(Long userId);
    
    void unlockUser(Long userId);
}
