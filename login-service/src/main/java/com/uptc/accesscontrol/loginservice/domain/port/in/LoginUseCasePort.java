package com.uptc.accesscontrol.loginservice.domain.port.in;

import com.uptc.accesscontrol.loginservice.application.dto.AuthRequest;
import com.uptc.accesscontrol.loginservice.application.dto.AuthResponse;
import com.uptc.accesscontrol.loginservice.application.dto.CreateUserRequest;
import com.uptc.accesscontrol.loginservice.application.dto.CreateUserResponse;

public interface LoginUseCasePort {
    
    CreateUserResponse createUser(CreateUserRequest request);
    
    AuthResponse authenticateUser(AuthRequest request);
}
