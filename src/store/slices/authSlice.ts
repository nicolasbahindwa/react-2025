import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { AuthState, RegisterResponse } from '@/features/Auth/types/auth.types';

const initialState: AuthState = {
  user: null,
  isAuthenticated: false,
  loading: false,
  error: null,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setUser: (state, action: PayloadAction<RegisterResponse>) => {
      state.user = action.payload;
      state.isAuthenticated = true;
      state.error = null;
    },
    clearUser: (state) => {
      state.user = null;
      state.isAuthenticated = false;
    },
    setError: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
    },
  },
});

export const { setUser, clearUser, setError } = authSlice.actions;
export default authSlice.reducer;
