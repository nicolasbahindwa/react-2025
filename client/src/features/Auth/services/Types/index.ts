export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
  terms: boolean;
}

export interface RegisterResponse {
  id: string;
  username: string;
  email: string;
}

export interface RegisterState {
  user: RegisterResponse | null
  status: 'idle' | 'loading' | 'succeeded' | 'failed';
  error: string | null;
}



export interface LoginRequest {
  email: string;     // The email address for login
  password: string;  // The password for login
}


export interface LoginResponse {
  accessToken: string;  // The access token for authentication
  refreshToken: string; // The refresh token for session renewal
  user: {
    id: string;
    username: string;
    email: string;
  };
}

export interface AuthState {
  user: LoginResponse | null;
  isAuthenticated: boolean;
  status: 'idle' | 'loading' | 'succeeded' | 'failed';
  error: string | null;
}

