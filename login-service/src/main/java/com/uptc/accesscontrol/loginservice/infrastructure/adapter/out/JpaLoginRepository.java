package com.uptc.accesscontrol.loginservice.infrastructure.adapter.out;

import com.uptc.accesscontrol.loginservice.domain.model.Login;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface JpaLoginRepository extends JpaRepository<Login, Long> {
    
    Optional<Login> findByUserId(Long userId);
    
    boolean existsByUserId(Long userId);
}
