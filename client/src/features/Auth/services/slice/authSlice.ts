import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { AuthState, LoginResponse } from "../Types/auth.types";

const initialState: AuthState = {
  user: null,
  tokens: {
    accessToken: '',
    refreshToken: '',
    accessTokenExpiresIn: 0,
    refreshTokenExpiresIn: 0,
  },
  isAuthenticated: false,
  status: "idle",
  error: null,
  lastLoginTime: null,
  sessionExpiresAt: null,
};

const calculateSessionExpiry = (expiresIn: number): string => {
  return new Date(Date.now() + expiresIn * 1000).toISOString();
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setCredentials: (state, action: PayloadAction<LoginResponse>) => {
      state.user = action.payload.user;
      state.tokens = {
        accessToken: action.payload.accessToken,
        refreshToken: action.payload.refreshToken,
        accessTokenExpiresIn: action.payload.accessTokenExpiresIn,
        refreshTokenExpiresIn: action.payload.refreshTokenExpiresIn,
      };
      state.isAuthenticated = true;
      state.status = "succeeded";
      state.error = null;
      state.lastLoginTime = new Date().toISOString();
      state.sessionExpiresAt = calculateSessionExpiry(action.payload.accessTokenExpiresIn);
    },
    updateAccessToken: (
      state,
      action: PayloadAction<{ accessToken: string; accessTokenExpiresIn: number }>
    ) => {
      state.tokens.accessToken = action.payload.accessToken;
      state.tokens.accessTokenExpiresIn = action.payload.accessTokenExpiresIn;
      state.sessionExpiresAt = calculateSessionExpiry(action.payload.accessTokenExpiresIn);
    },
    clearCredentials: () => initialState,
    setLoading: (state) => {
      state.status = "loading";
      state.error = null;
    },
    setError: (state, action: PayloadAction<string>) => {
      state.status = "failed";
      state.error = action.payload;
    },
  },
});

export const {
  setCredentials,
  updateAccessToken,
  clearCredentials,
  setLoading,
  setError,
} = authSlice.actions;

// Typed selectors
export const selectCurrentUser = (state: { auth: AuthState }) =>
  state.auth.user;
export const selectAuthTokens = (state: { auth: AuthState }) =>
  state.auth.tokens;
export const selectIsAuthenticated = (state: { auth: AuthState }) =>
  state.auth.isAuthenticated;
export const selectAuthStatus = (state: { auth: AuthState }) =>
  state.auth.status;
export const selectAuthError = (state: { auth: AuthState }) =>
  state.auth.error;
export const selectSessionExpiresAt = (state: { auth: AuthState }) =>
  state.auth.sessionExpiresAt;

export default authSlice.reducer;
