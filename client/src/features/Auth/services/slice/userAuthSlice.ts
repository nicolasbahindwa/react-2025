// src/store/slices/authSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import type { RegisterState, RegisterResponse } from '../Types';
import { RootState } from '../../../../store/index';
 
const initialState: RegisterState = {
  user: null,
  status: 'idle',
  error: null,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setUser: (state, action: PayloadAction<RegisterResponse>) => {
      state.user = action.payload;
      state.status = 'succeeded';
      state.error = null;
    },
    setStatus: (state, action: PayloadAction<RegisterState['status']>) => {
      state.status = action.payload;
      if (action.payload === 'loading') {
        state.error = null;
      }
    },
    setError: (state, action: PayloadAction<string>) => {
      state.status = 'failed';
      state.error = action.payload;
    },
    clearUser: (state) => {
      state.user = null;
      state.status = 'idle';
      state.error = null;
    },
  },
});

export const { setUser, setStatus, setError, clearUser } = authSlice.actions;

export default authSlice.reducer;



// Fixing the TypeScript error caused by PersistPartial
export const selectUser = (state: RootState): RegisterResponse | null =>
  (state as any).auth.user; // Alternatively, cast to RootState if PersistPartial issues persist

export const selectAuthStatus = (state: RootState): RegisterState['status'] =>
  (state as any).auth.status;

export const selectAuthError = (state: RootState): string | null =>
  (state as any).auth.error;

export const selectIsAuthenticated = (state: RootState): boolean =>
  (state as any).auth.user !== null;
 

 