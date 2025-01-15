import { persistReducer, createTransform, PersistedState } from 'redux-persist';
import storage from 'redux-persist/lib/storage';
import { rootReducer } from './reducers';
import { baseApi } from '@/lib/baseApi';

// Custom transform to handle serialization of dates
const dateTransform = createTransform(
  // transform state on its way to being serialized and persisted
  (inboundState: any) => {
    return {
      ...inboundState,
      lastLoginTime: inboundState.lastLoginTime?.toISOString(),
      sessionExpiresAt: inboundState.sessionExpiresAt?.toISOString(),
    };
  },
  // transform state being rehydrated
  (outboundState: any) => {
    return {
      ...outboundState,
      lastLoginTime: outboundState.lastLoginTime ? new Date(outboundState.lastLoginTime) : null,
      sessionExpiresAt: outboundState.sessionExpiresAt ? new Date(outboundState.sessionExpiresAt) : null,
    };
  },
  // define which reducers this transform gets called for
  { whitelist: ['auth'] }
);

const persistConfig = {
  key: 'root',
  version: 1,
  storage,
  whitelist: ['auth'], // Only persist auth
  blacklist: [baseApi.reducerPath], // Don't persist API cache
  transforms: [dateTransform],
  throttle: 1000, // Throttle storage writes
  migrate: (state: PersistedState, version: number) => {
    // Handle migrations between versions
    if (!state) {
      return Promise.resolve(undefined);
    }
    // Perform any necessary migrations here
    return Promise.resolve(state);
  },
};

export const persistedReducer = persistReducer(persistConfig, rootReducer);