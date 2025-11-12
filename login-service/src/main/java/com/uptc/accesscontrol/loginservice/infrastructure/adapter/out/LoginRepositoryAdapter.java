package com.uptc.accesscontrol.loginservice.infrastructure.adapter.out;

import com.uptc.accesscontrol.loginservice.domain.model.Login;
import com.uptc.accesscontrol.loginservice.domain.port.out.LoginRepositoryPort;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.util.Optional;

@Component
@RequiredArgsConstructor
public class LoginRepositoryAdapter implements LoginRepositoryPort {

    private final JpaLoginRepository jpaLoginRepository;

    @Override
    public Login save(Login login) {
        return jpaLoginRepository.save(login);
    }

    @Override
    public Optional<Login> findByUserId(Long userId) {
        return jpaLoginRepository.findByUserId(userId);
    }

    @Override
    public boolean existsByUserId(Long userId) {
        return jpaLoginRepository.existsByUserId(userId);
    }

    @Override
    public void updateFailedAttempts(Long userId, int attempts) {
        jpaLoginRepository.findByUserId(userId).ifPresent(login -> {
            login.setFailedAttempts(attempts);
            jpaLoginRepository.save(login);
        });
    }

    @Override
    public void lockUser(Long userId) {
        jpaLoginRepository.findByUserId(userId).ifPresent(login -> {
            login.setIsLocked(true);
            login.setLockTime(LocalDateTime.now());
            jpaLoginRepository.save(login);
        });
    }

    @Override
    public void unlockUser(Long userId) {
        jpaLoginRepository.findByUserId(userId).ifPresent(login -> {
            login.setIsLocked(false);
            login.setFailedAttempts(0);
            login.setLockTime(null);
            jpaLoginRepository.save(login);
        });
    }
}
