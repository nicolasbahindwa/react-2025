export interface FormRegister {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
  terms: boolean;
}

export interface FormLogin {
  email: string;       
  password: string;  
  rememberMe: boolean;  
}


// store

export interface RegisterResponse {
  id: string;
  username: string;
  email: string;
  token: string;
}

export interface AuthState {
  user: RegisterResponse | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
}