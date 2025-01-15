export interface RegisterRequest {
    id?: string;
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
    user: RegisterResponse | null;
    status: 'idle' | 'loading' | 'succeeded' | 'failed';
    error: string | null;
  }
  