// store/middleware/index.ts
import { authMiddleware } from './authMiddleware';
import { baseApi } from '@/lib/baseApi';
import rtkQueryErrorLogger from './rtkQueryErrorLogger';
import { 
  FLUSH, 
  REHYDRATE, 
  PAUSE, 
  PERSIST, 
  PURGE, 
  REGISTER 
} from 'redux-persist';
import { Middleware } from '@reduxjs/toolkit';
import { RootState } from '../types';

type AppMiddleware = Middleware<{}, RootState>;

export const getMiddleware = (getDefaultMiddleware: any) => {
  const middleware = getDefaultMiddleware({
    serializableCheck: {
      ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      ignoredPaths: [
        'register',
        'rehydrate',
        'auth.tokens',
        'auth.sessionExpiresAt',
      ],
    },
    immutableCheck: { warnAfter: 128 },
  });

  const customMiddleware: AppMiddleware[] = [
    authMiddleware,
    baseApi.middleware,
    rtkQueryErrorLogger,
  ];

  return middleware.concat(customMiddleware);
};