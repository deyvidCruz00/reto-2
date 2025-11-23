package com.uptc.accesscontrol.loginservice.infrastructure.adapter.out;

import com.uptc.accesscontrol.loginservice.domain.model.LoginDomain;
import com.uptc.accesscontrol.loginservice.domain.port.out.LoginRepositoryPort;
import com.uptc.accesscontrol.loginservice.infrastructure.persistence.LoginJpaEntity;
import com.uptc.accesscontrol.loginservice.infrastructure.persistence.LoginMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.util.Optional;

@Component
@RequiredArgsConstructor
public class LoginRepositoryAdapter implements LoginRepositoryPort {

    private final JpaLoginRepository jpaLoginRepository;
    private final LoginMapper loginMapper;

    @Override
    public LoginDomain save(LoginDomain login) {
        LoginJpaEntity jpaEntity = loginMapper.toJpaEntity(login);
        LoginJpaEntity saved = jpaLoginRepository.save(jpaEntity);
        return loginMapper.toDomain(saved);
    }

    @Override
    public Optional<LoginDomain> findByUserId(Long userId) {
        return jpaLoginRepository.findByUserId(userId)
                .map(loginMapper::toDomain);
    }

    @Override
    public boolean existsByUserId(Long userId) {
        return jpaLoginRepository.existsByUserId(userId);
    }

    @Override
    public void updateFailedAttempts(Long userId, int attempts) {
        jpaLoginRepository.findByUserId(userId).ifPresent(jpaEntity -> {
            jpaEntity.setFailedAttempts(attempts);
            jpaEntity.setUpdatedAt(LocalDateTime.now());
            jpaLoginRepository.save(jpaEntity);
        });
    }

    @Override
    public void lockUser(Long userId) {
        jpaLoginRepository.findByUserId(userId).ifPresent(jpaEntity -> {
            jpaEntity.setIsLocked(true);
            jpaEntity.setLockTime(LocalDateTime.now());
            jpaEntity.setUpdatedAt(LocalDateTime.now());
            jpaLoginRepository.save(jpaEntity);
        });
    }

    @Override
    public void unlockUser(Long userId) {
        jpaLoginRepository.findByUserId(userId).ifPresent(jpaEntity -> {
            jpaEntity.setIsLocked(false);
            jpaEntity.setFailedAttempts(0);
            jpaEntity.setLockTime(null);
            jpaEntity.setUpdatedAt(LocalDateTime.now());
            jpaLoginRepository.save(jpaEntity);
        });
    }
}
