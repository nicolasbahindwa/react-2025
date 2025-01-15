import { Middleware } from '@reduxjs/toolkit';
import { RootState } from '../types';
import { clearCredentials } from '@/features/Auth/services/slice/authSlice';

export const authMiddleware: Middleware<{}, RootState> = (store) => (next) => (action) => {
  const result = next(action);
  const state = store.getState();

  // Check for token expiration
  if (state.auth.tokens?.accessToken) {
    const expirationTime = new Date(state.auth.sessionExpiresAt || '').getTime();
    const currentTime = new Date().getTime();

    if (currentTime >= expirationTime) {
      store.dispatch(clearCredentials());
      window.location.href = '/login';
    }
  }

  return result;
};
