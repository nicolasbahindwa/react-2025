import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { RegisterState, RegisterResponse } from "../Types/user.types";

const initialState: RegisterState = {
  user: null,
  status: 'idle',
  error: null,
};

const userAuthSlice = createSlice({
  name: 'userAuth',
  initialState,
  reducers: {
    setUser: (state, action: PayloadAction<RegisterResponse>) => {
      state.user = action.payload;
      state.status = 'succeeded';
      state.error = null;
    },
    clearUser: (state) => {
      state.user = null;
      state.status = 'idle';
      state.error = null;
    },
    setStatus: (state, action: PayloadAction<'idle' | 'loading' | 'succeeded' | 'failed'>) => {
      state.status = action.payload;
    },
    setError: (state, action: PayloadAction<string>) => {
      state.status = 'failed';
      state.error = action.payload;
    },
  },
});

export const {
  setUser,
  clearUser,
  setStatus,
  setError,
} = userAuthSlice.actions;

// Typed selectors
export const selectCurrentUser = (state: { userAuth: RegisterState }) => state.userAuth.user;
export const selectRegisterStatus = (state: { userAuth: RegisterState }) => state.userAuth.status;
export const selectRegisterError = (state: { userAuth: RegisterState }) => state.userAuth.error;

export default userAuthSlice.reducer;
