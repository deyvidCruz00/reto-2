package com.uptc.accesscontrol.loginservice.infrastructure.adapter.out;

import com.uptc.accesscontrol.loginservice.infrastructure.persistence.LoginJpaEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface JpaLoginRepository extends JpaRepository<LoginJpaEntity, Long> {
    
    Optional<LoginJpaEntity> findByUserId(Long userId);
    
    boolean existsByUserId(Long userId);
}
