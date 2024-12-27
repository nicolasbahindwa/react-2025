import { createApi, fetchBaseQuery, FetchArgs, FetchBaseQueryError } from '@reduxjs/toolkit/query/react';
import { RootState } from '@/store';
import { clearUser } from '@/features/Auth/services/slice';
import { ENV } from '@/config/environment';

const baseQuery = fetchBaseQuery({
  baseUrl: ENV.API_BASE_URL,
  prepareHeaders: (headers, { getState }) => {
    const token = (getState() as RootState).auth.user?.token;
    if (token) {
      headers.set('Authorization', `Bearer ${token}`);
    }
    return headers;
  },
});

const baseQueryWithReauth = async (args: string | FetchArgs, api: any, extraOptions: {}) => {
  const result = await baseQuery(args, api, extraOptions);
  
  if (result.error?.status === 401) {
    api.dispatch(clearUser());
    // Redirect to login page
    window.location.href = '/login';
  }
  
  return result;
};

export const baseApi = createApi({
  baseQuery: baseQueryWithReauth,
  endpoints: () => ({}),
  tagTypes: ['Auth'],
});