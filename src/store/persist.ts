import { persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';
import { rootReducer } from './reducers';
import { baseApi } from '@/lib/api/baseApi';

const persistConfig = {
  key: 'root',
  version: 1,
  storage,
  whitelist: ['auth'], // Only persist auth
  blacklist: [baseApi.reducerPath], // Don't persist API cache
  // You can add transforms if needed
  // transforms: [],
};

export const persistedReducer = persistReducer(persistConfig, rootReducer);