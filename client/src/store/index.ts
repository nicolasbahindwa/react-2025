import { configureStore } from '@reduxjs/toolkit';
import { persistStore } from 'redux-persist';
import { ENV } from '@/config/environment';
import { persistedReducer } from './persist';
import { getMiddleware } from './middleware';
import { getEnhancers } from './enhancers';

export const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) => getMiddleware(getDefaultMiddleware),
  enhancers: getEnhancers, // Directly pass getEnhancers
  devTools: ENV.nodeEnv !== 'production', // Enable DevTools in non-production environments
});

export const persistor = persistStore(store);

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;