export interface RegisterRequest {
  id?:string;
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



export interface AuthUser {
  id: string;
  email: string;
  name: string;
  roles: string[];
}

export interface AuthTokens {
  accessToken: string | null;
  refreshToken: string | null;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  user: AuthUser;
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}

export interface AuthState {
  user: AuthUser | null;
  tokens: AuthTokens;
  isAuthenticated: boolean;
  status: "idle" | "loading" | "succeeded" | "failed";
  error: string | null;
  lastLoginTime: string | null;
  sessionExpiresAt: string | null;
}
