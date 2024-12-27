import { configureStore } from '@reduxjs/toolkit';
import { persistStore } from 'redux-persist';
import { ENV } from '@/config/environment';
import { persistedReducer } from './persist';
import { getMiddleware } from './middleware';
import { getEnhancers } from './enhancers';

export const store = configureStore({
  reducer: persistedReducer,
  middleware: getMiddleware,
  enhancers: getEnhancers,
  devTools: ENV.NODE_ENV !== 'production',
});

export const persistor = persistStore(store);

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
