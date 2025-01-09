import { createAsyncThunk } from '@reduxjs/toolkit';
import { baseApi } from '@/lib/api/baseApi';
import { setUser, setError, setLoading } from '@/features/Auth/services/slice';
import type { RegisterRequest, RegisterResponse } from '@/features/Auth/types';

export const registerUser = createAsyncThunk<RegisterResponse, RegisterRequest>(
  'auth/registerUser',
  async (credentials, { dispatch }) => {
    try {
      dispatch(setLoading(true));
      const response = await dispatch(baseApi.endpoints.register.initiate(credentials)).unwrap();
      dispatch(setUser(response));
      return response;
    } catch (error: any) {
      dispatch(setError(error.message || 'Registration failed. Please try again.'));
      throw error;
    } finally {
      dispatch(setLoading(false));
    }
  }
);
