package com.uptc.accesscontrol.loginservice.infrastructure.adapter.in;

import com.uptc.accesscontrol.loginservice.application.dto.*;
import com.uptc.accesscontrol.loginservice.domain.port.in.LoginUseCasePort;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/login")
@RequiredArgsConstructor
@Slf4j
@Tag(name = "Login", description = "Login and Authentication API")
public class LoginController {

    private final LoginUseCasePort loginUseCase;

    @PostMapping("/createuser")
    @Operation(summary = "Create a new user", description = "Register a new user in the system")
    public ResponseEntity<CreateUserResponse> createUser(@Valid @RequestBody CreateUserRequest request) {
        log.info("Creating user: {}", request.getUserId());
        CreateUserResponse response = loginUseCase.createUser(request);
        
        return response.isSuccess() 
                ? ResponseEntity.status(HttpStatus.CREATED).body(response)
                : ResponseEntity.status(HttpStatus.BAD_REQUEST).body(response);
    }

    @PostMapping("/authuser")
    @Operation(summary = "Authenticate user", description = "Authenticate user and generate JWT token")
    public ResponseEntity<AuthResponse> authenticateUser(@Valid @RequestBody AuthRequest request) {
        log.info("Authenticating user: {}", request.getUserId());
        AuthResponse response = loginUseCase.authenticateUser(request);
        
        if (response.isSuccess()) {
            return ResponseEntity.ok(response);
        } else if (response.isLocked()) {
            return ResponseEntity.status(HttpStatus.LOCKED).body(response);
        } else {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(response);
        }
    }
}
