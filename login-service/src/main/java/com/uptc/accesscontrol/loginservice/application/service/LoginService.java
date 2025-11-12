package com.uptc.accesscontrol.loginservice.application.service;

import com.uptc.accesscontrol.loginservice.application.dto.*;
import com.uptc.accesscontrol.loginservice.domain.model.Login;
import com.uptc.accesscontrol.loginservice.domain.port.in.LoginUseCasePort;
import com.uptc.accesscontrol.loginservice.domain.port.out.LoginRepositoryPort;
import com.uptc.accesscontrol.loginservice.infrastructure.event.AlertEventPublisher;
import com.uptc.accesscontrol.loginservice.infrastructure.security.JwtTokenProvider;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.time.Duration;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class LoginService implements LoginUseCasePort {

    private final LoginRepositoryPort loginRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtTokenProvider jwtTokenProvider;
    private final AlertEventPublisher alertEventPublisher;

    @Value("${login.max-attempts}")
    private int maxAttempts;

    @Value("${login.lock-duration-minutes}")
    private int lockDurationMinutes;

    @Override
    @Transactional
    public CreateUserResponse createUser(CreateUserRequest request) {
        try {
            // Verificar si el usuario ya existe
            if (loginRepository.existsByUserId(request.getUserId())) {
                return CreateUserResponse.builder()
                        .userId(request.getUserId())
                        .message("User already exists")
                        .success(false)
                        .build();
            }

            // Crear nuevo usuario
            Login login = Login.builder()
                    .userId(request.getUserId())
                    .password(passwordEncoder.encode(request.getPassword()))
                    .isLocked(false)
                    .failedAttempts(0)
                    .build();

            Login savedLogin = loginRepository.save(login);

            log.info("User created successfully: {}", savedLogin.getUserId());

            return CreateUserResponse.builder()
                    .userId(savedLogin.getUserId())
                    .message("User created successfully")
                    .success(true)
                    .build();

        } catch (Exception e) {
            log.error("Error creating user: {}", e.getMessage());
            return CreateUserResponse.builder()
                    .userId(request.getUserId())
                    .message("Error creating user: " + e.getMessage())
                    .success(false)
                    .build();
        }
    }

    @Override
    @Transactional
    public AuthResponse authenticateUser(AuthRequest request) {
        try {
            Optional<Login> loginOpt = loginRepository.findByUserId(request.getUserId());

            // Usuario no registrado
            if (loginOpt.isEmpty()) {
                log.warn("Authentication attempt for non-existing user: {}", request.getUserId());
                alertEventPublisher.publishUserNotRegisteredAlert(request.getUserId());
                
                return AuthResponse.builder()
                        .userId(request.getUserId())
                        .message("Invalid credentials")
                        .success(false)
                        .locked(false)
                        .build();
            }

            Login login = loginOpt.get();

            // Verificar si el usuario está bloqueado
            if (login.getIsLocked() && login.getLockTime() != null) {
                LocalDateTime unlockTime = login.getLockTime().plusMinutes(lockDurationMinutes);
                
                if (LocalDateTime.now().isBefore(unlockTime)) {
                    long minutesRemaining = Duration.between(LocalDateTime.now(), unlockTime).toMinutes();
                    log.warn("User {} is locked. Unlock in {} minutes", request.getUserId(), minutesRemaining);
                    
                    return AuthResponse.builder()
                            .userId(request.getUserId())
                            .message("Account locked. Try again in " + minutesRemaining + " minutes")
                            .success(false)
                            .locked(true)
                            .build();
                } else {
                    // Desbloquear usuario si ya pasó el tiempo
                    loginRepository.unlockUser(request.getUserId());
                    login.setIsLocked(false);
                    login.setFailedAttempts(0);
                }
            }

            // Verificar contraseña
            if (!passwordEncoder.matches(request.getPassword(), login.getPassword())) {
                int newAttempts = login.getFailedAttempts() + 1;
                loginRepository.updateFailedAttempts(request.getUserId(), newAttempts);

                log.warn("Failed login attempt for user {}. Attempt {}/{}", 
                        request.getUserId(), newAttempts, maxAttempts);

                // Bloquear usuario si excede los intentos
                if (newAttempts >= maxAttempts) {
                    loginRepository.lockUser(request.getUserId());
                    alertEventPublisher.publishUserExceededAttemptsAlert(request.getUserId());
                    
                    log.warn("User {} locked due to exceeded login attempts", request.getUserId());
                    
                    return AuthResponse.builder()
                            .userId(request.getUserId())
                            .message("Account locked due to multiple failed attempts. Try again in " + 
                                    lockDurationMinutes + " minutes")
                            .success(false)
                            .locked(true)
                            .build();
                }

                return AuthResponse.builder()
                        .userId(request.getUserId())
                        .message("Invalid credentials. Attempts: " + newAttempts + "/" + maxAttempts)
                        .success(false)
                        .locked(false)
                        .build();
            }

            // Autenticación exitosa - resetear intentos
            if (login.getFailedAttempts() > 0) {
                loginRepository.updateFailedAttempts(request.getUserId(), 0);
            }

            // Generar token JWT
            String token = jwtTokenProvider.generateToken(request.getUserId());

            log.info("User {} authenticated successfully", request.getUserId());

            return AuthResponse.builder()
                    .userId(request.getUserId())
                    .token(token)
                    .message("Authentication successful")
                    .success(true)
                    .locked(false)
                    .build();

        } catch (Exception e) {
            log.error("Error authenticating user: {}", e.getMessage());
            return AuthResponse.builder()
                    .userId(request.getUserId())
                    .message("Authentication error: " + e.getMessage())
                    .success(false)
                    .locked(false)
                    .build();
        }
    }
}
