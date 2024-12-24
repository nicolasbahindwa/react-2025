// Form Data Types
export interface RegisterFormData {
    email: string;
    password: string;
    confirmPassword: string;
    firstName: string;
    lastName: string;
    phoneNumber: string;
  }
  
  // API Request Types
  export interface RegisterRequestData extends Omit<RegisterFormData, 'confirmPassword'> {
    // Omitting confirmPassword as it's not needed for API request
  }
  
  // API Response Types
  export interface RegisterResponseData {
    user: {
      id: string;
      email: string;
      firstName: string;
      lastName: string;
      phoneNumber: string;
      createdAt: string;
      updatedAt: string;
    };
    token: string;
  }
  
  // Error Types
  export interface AuthError {
    message: string;
    code: string;
    field?: string;
  }
  
  // Auth State Types
  export interface AuthState {
    user: RegisterResponseData['user'] | null;
    token: string | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    error: AuthError | null;
  }