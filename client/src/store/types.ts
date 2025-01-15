// store/types.ts
import { Action, ThunkAction } from '@reduxjs/toolkit';
import { baseApi } from '@/lib/baseApi';
import authReducer from '@/features/Auth/services/slice/authSlice';
import userAuthSlice from '@/features/Auth/services/slice/userRegistrationAction';

// Define the store shape
type ApiReducers = {
    [key in typeof baseApi.reducerPath]: ReturnType<typeof baseApi.reducer>;
  };
  
  export interface StoreShape extends ApiReducers {
    auth: ReturnType<typeof authReducer>;
    userAuth: ReturnType<typeof userAuthSlice>;
  }

// Export types for use throughout the app
export type AppDispatch = {
  <ReturnType = void>(
    action: Action | ThunkAction<ReturnType, StoreShape, unknown, Action>
  ): ReturnType;
};

export type RootState = StoreShape;

// You might also want to add a helper type for thunks
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;
