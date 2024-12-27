import { combineReducers } from '@reduxjs/toolkit';
import { baseApi } from '@/lib/api/baseApi';
import authReducer from '@/features/Auth/services/slice';

export const rootReducer = combineReducers({
  [baseApi.reducerPath]: baseApi.reducer,
  auth: authReducer,
});