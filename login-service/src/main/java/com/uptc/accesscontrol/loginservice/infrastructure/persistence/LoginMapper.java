package com.uptc.accesscontrol.loginservice.infrastructure.persistence;

import com.uptc.accesscontrol.loginservice.domain.model.LoginDomain;
import org.springframework.stereotype.Component;

/**
 * Mapper between Domain and JPA entities
 * Ensures domain remains pure without infrastructure dependencies
 */
@Component
public class LoginMapper {

    /**
     * Convert JPA entity to Domain entity
     */
    public LoginDomain toDomain(LoginJpaEntity jpaEntity) {
        if (jpaEntity == null) {
            return null;
        }

        return new LoginDomain(
            jpaEntity.getId(),
            jpaEntity.getUserId(),
            jpaEntity.getPassword(),
            jpaEntity.getIsLocked(),
            jpaEntity.getFailedAttempts(),
            jpaEntity.getLockTime(),
            jpaEntity.getCreatedAt(),
            jpaEntity.getUpdatedAt()
        );
    }

    /**
     * Convert Domain entity to JPA entity
     */
    public LoginJpaEntity toJpaEntity(LoginDomain domain) {
        if (domain == null) {
            return null;
        }

        return LoginJpaEntity.builder()
            .id(domain.getId())
            .userId(domain.getUserId())
            .password(domain.getPassword())
            .isLocked(domain.getIsLocked())
            .failedAttempts(domain.getFailedAttempts())
            .lockTime(domain.getLockTime())
            .createdAt(domain.getCreatedAt())
            .updatedAt(domain.getUpdatedAt())
            .build();
    }

    /**
     * Update JPA entity from Domain entity (preserving JPA managed state)
     */
    public void updateJpaEntity(LoginJpaEntity jpaEntity, LoginDomain domain) {
        if (jpaEntity == null || domain == null) {
            return;
        }

        jpaEntity.setUserId(domain.getUserId());
        jpaEntity.setPassword(domain.getPassword());
        jpaEntity.setIsLocked(domain.getIsLocked());
        jpaEntity.setFailedAttempts(domain.getFailedAttempts());
        jpaEntity.setLockTime(domain.getLockTime());
        jpaEntity.setUpdatedAt(domain.getUpdatedAt());
    }
}
