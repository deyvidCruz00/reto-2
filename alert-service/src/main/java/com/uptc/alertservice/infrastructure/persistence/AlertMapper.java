package com.uptc.alertservice.infrastructure.persistence;

import com.uptc.alertservice.domain.entity.AlertDomain;
import org.springframework.stereotype.Component;

/**
 * Mapper between Domain and JPA entities for Alert
 * Ensures domain remains pure without infrastructure dependencies
 */
@Component
public class AlertMapper {

    /**
     * Convert JPA entity to Domain entity
     */
    public AlertDomain toDomain(AlertJpaEntity jpaEntity) {
        if (jpaEntity == null) {
            return null;
        }

        return new AlertDomain(
            jpaEntity.getId(),
            jpaEntity.getTimestamp(),
            jpaEntity.getDescription(),
            jpaEntity.getCode(),
            jpaEntity.getSeverity(),
            jpaEntity.getEmployeeId(),
            jpaEntity.getUserId(),
            jpaEntity.getAdditionalInfo()
        );
    }

    /**
     * Convert Domain entity to JPA entity
     */
    public AlertJpaEntity toJpaEntity(AlertDomain domain) {
        if (domain == null) {
            return null;
        }

        return AlertJpaEntity.builder()
            .id(domain.getId())
            .timestamp(domain.getTimestamp())
            .description(domain.getDescription())
            .code(domain.getCode())
            .severity(domain.getSeverity())
            .employeeId(domain.getEmployeeId())
            .userId(domain.getUserId())
            .additionalInfo(domain.getAdditionalInfo())
            .build();
    }

    /**
     * Update JPA entity from Domain entity (preserving JPA managed state)
     */
    public void updateJpaEntity(AlertJpaEntity jpaEntity, AlertDomain domain) {
        if (jpaEntity == null || domain == null) {
            return;
        }

        jpaEntity.setTimestamp(domain.getTimestamp());
        jpaEntity.setDescription(domain.getDescription());
        jpaEntity.setCode(domain.getCode());
        jpaEntity.setSeverity(domain.getSeverity());
        jpaEntity.setEmployeeId(domain.getEmployeeId());
        jpaEntity.setUserId(domain.getUserId());
        jpaEntity.setAdditionalInfo(domain.getAdditionalInfo());
    }
}
