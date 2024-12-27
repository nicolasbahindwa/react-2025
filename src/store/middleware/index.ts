import { Middleware } from '@reduxjs/toolkit';
import { baseApi } from '@/lib/api/baseApi';
import rtkQueryErrorLogger from './rtkQueryErrorLogger';
import {
  FLUSH,
  REHYDRATE,
  PAUSE,
  PERSIST,
  PURGE,
  REGISTER
} from 'redux-persist';

export const getMiddleware = (getDefaultMiddleware: any) => {
  const middleware = getDefaultMiddleware({
    serializableCheck: {
      ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      // Optionally, you can also ignore specific paths in your state
      ignoredPaths: ['register', 'rehydrate'],
    },
    // If you have immutability issues, you can also configure this
    immutableCheck: { warnAfter: 128 },
  });

  return middleware.concat([
    baseApi.middleware,
    rtkQueryErrorLogger,
  ]);
};