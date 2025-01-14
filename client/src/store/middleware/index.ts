// import { Middleware } from '@reduxjs/toolkit';
// import { baseApi } from '@/lib/baseApi';
// import { userApi } from '../../features/Auth/services/actions/userRegistrationAction';
// import { authApi } from '../../features/Auth/services/actions/authActions';
// import rtkQueryErrorLogger from './rtkQueryErrorLogger';
// import {
//   FLUSH,
//   REHYDRATE,
//   PAUSE,
//   PERSIST,
//   PURGE,
//   REGISTER
// } from 'redux-persist';

// export const getMiddleware = (getDefaultMiddleware: any) => {
//   const middleware = getDefaultMiddleware({
//     serializableCheck: {
//       ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
//       // Optionally, you can also ignore specific paths in your state
//       ignoredPaths: ['register', 'rehydrate'],
//     },
//     // If you have immutability issues, you can also configure this
//     immutableCheck: { warnAfter: 128 },
//   });

//   return middleware.concat([
//     baseApi.middleware,
//     userApi.middleware,
//     authApi.middleware,
//     rtkQueryErrorLogger,
//   ]);
// };


// store/middleware/index.ts
import { authMiddleware } from '@/features/Auth/middleware/authMiddleware';
import { baseApi } from '@/lib/baseApi';
import { userApi } from '../../features/Auth/services/actions/userRegistrationAction';
import { authApi } from '../../features/Auth/services/actions/authActions';
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
      ignoredPaths: ['register', 'rehydrate'],
    },
    immutableCheck: { warnAfter: 128 },
  });

  return middleware.concat([
    authMiddleware, // Add the auth middleware
    baseApi.middleware,
    userApi.middleware,
    authApi.middleware,
    rtkQueryErrorLogger,
  ]);
};