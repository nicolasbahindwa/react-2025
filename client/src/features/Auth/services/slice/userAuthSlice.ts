import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import type { RegisterResponse, RegisterState } from '../Types';

const initialState: RegisterState = {
  user: null,
  status: 'idle',
  error: null,
};

const userAuthSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    // Handle setting an error state
    setError: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
      state.status = 'failed';
    },
    // Handle setting user data after successful registration
    setUser: (state, action: PayloadAction<RegisterResponse>) => {
      state.status = 'succeeded';
      state.user = action.payload;
    },
    // Handle setting loading status during an async operation
    setLoading: (state, action: PayloadAction<boolean>) => { 
      state.status = action.payload ? 'loading' : 'idle';
      if (!action.payload) {
         state.error = null;
      } 
    },
    // Example of an extra reducer to handle specific state changes
    extraReducerExample: (state) => {
      // Implementation of state changes here
    },
  },
});

export const { setUser, setError, setLoading } = userAuthSlice.actions;

export default userAuthSlice.reducer;
