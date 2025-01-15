import { combineReducers } from '@reduxjs/toolkit';
import { baseApi } from '@/lib/baseApi';
import authReducer from '@/features/Auth/services/slice/authSlice';
import userAuthSlice from '@/features/Auth/services/slice/userAuthSlice';

export const rootReducer = combineReducers({
  [baseApi.reducerPath]: baseApi.reducer,
    auth: authReducer,
    userAuth: userAuthSlice,
});

 