export interface FormRegister {
    username: string;        // The username field, which should be a string
    email: string;           // The email field, which should be a string
    password: string;        // The password field, which should be a string
    confirmPassword: string; // The confirm password field, which should be a string
    terms: boolean;          // The terms and conditions checkbox, which should be a boolean (checked or not)
  }
  