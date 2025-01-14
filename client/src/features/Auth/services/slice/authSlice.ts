// import { createSlice, PayloadAction } from '@reduxjs/toolkit';
// import { AuthState, LoginResponse } from '../Types';

// const initialState: AuthState = {
//   user: null,
//   tokens: {
//     accessToken: null,
//     refreshToken: null,
//   },
//   isAuthenticated: false,
//   status: 'idle',
//   error: null,
// };

// const authSlice = createSlice({
//   name: 'auth',
//   initialState,
//   reducers: {
//     setCredentials: (state, action: PayloadAction<LoginResponse>) => {
//       state.user = action.payload;
//       state.tokens = {
//         accessToken: action.payload.accessToken,
//         refreshToken: action.payload.refreshToken,
//       };
//       state.isAuthenticated = true;
//       state.status = 'succeeded';
//       state.error = null;
//     },
//     clearCredentials: (state) => {
//       state.user = null;
//       state.tokens = {
//         accessToken: null,
//         refreshToken: null,
//       };
//       state.isAuthenticated = false;
//       state.status = 'idle';
//       state.error = null;
//     },
//     setLoading: (state) => {
//       state.status = 'loading';
//       state.error = null;
//     },
//     setError: (state, action: PayloadAction<string>) => {
//       state.status = 'failed';
//       state.error = action.payload;
//     },
//   },
// });

 

// export const { setCredentials, clearCredentials, setLoading, setError } = authSlice.actions;


// // Selectors
// export const selectCurrentUser = (state: { auth: AuthState }) => state.auth.user;
// export const selectAuthTokens = (state: { auth: AuthState }) => state.auth.tokens;
// export const selectIsAuthenticated = (state: { auth: AuthState }) => state.auth.isAuthenticated;
// export const selectAuthStatus = (state: { auth: AuthState }) => state.auth.status;
// export const selectAuthError = (state: { auth: AuthState }) => state.auth.error;
 
// export default authSlice.reducer;

import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { AuthState, LoginResponse } from "../Types/index";

const initialState: AuthState = {
  user: null,
  tokens: {
    accessToken: null,
    refreshToken: null,
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
      };
      state.isAuthenticated = true;
      state.status = "succeeded";
      state.error = null;
      state.lastLoginTime = new Date().toISOString();
      state.sessionExpiresAt = calculateSessionExpiry(action.payload.expiresIn);
    },
    updateAccessToken: (
      state,
      action: PayloadAction<{ accessToken: string; expiresIn: number }>
    ) => {
      state.tokens.accessToken = action.payload.accessToken;
      state.sessionExpiresAt = calculateSessionExpiry(action.payload.expiresIn);
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
export const selectAuthError = (state: { auth: AuthState }) => state.auth.error;
export const selectSessionExpiresAt = (state: { auth: AuthState }) =>
  state.auth.sessionExpiresAt;

export default authSlice.reducer;