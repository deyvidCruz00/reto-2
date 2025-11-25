export interface AuthRequest {
  userId: number;
  password: string;
}

export interface AuthResponse {
  userId: number;
  token: string | null;
  message: string;
  success: boolean;
  locked: boolean;
}

export interface CreateUserRequest {
  userId: number;
  password: string;
}

export interface CreateUserResponse {
  userId: number;
  message: string;
  success: boolean;
}
