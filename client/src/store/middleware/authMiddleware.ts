import { Middleware } from "@reduxjs/toolkit";
import { clearCredentials } from "../../features/Auth/services/slice/authSlice";

export const authMiddleware: Middleware = (store) => (next) => (action) => {
  const result = next(action);
  const state = store.getState();

  // Check for session expiration
  if (
    state.auth.sessionExpiresAt &&
    new Date(state.auth.sessionExpiresAt) <= new Date()
  ) {
    store.dispatch(clearCredentials());
    window.location.href = "/login";
  }

  return result;
};
