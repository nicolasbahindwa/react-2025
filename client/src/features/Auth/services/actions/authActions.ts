import { baseApi } from '@/lib/baseApi';
import { LoginRequest, LoginResponse, ApiEndpointBuilder } from '../Types/auth.types';
import {
  setCredentials,
  clearCredentials,
  setError,
  setLoading,
} from '../slice/authSlice';

 
// Your RTK Query setup looks great. Here are a few tweaks for readability and safety:

export const authApi = baseApi.injectEndpoints({
  endpoints: (build: ApiEndpointBuilder) => ({
    login: build.mutation<LoginResponse, LoginRequest>({
      query: (credentials: LoginRequest) => ({
        url: '/auth/login',
        method: 'POST',
        body: credentials,
      }),
      async onQueryStarted(
        credentials: LoginRequest,  
        { dispatch, queryFulfilled }: { dispatch: any; queryFulfilled: Promise<{ data: LoginResponse }> }
      ) {
        dispatch(setLoading());
        try {
          const { data } = await queryFulfilled;
          dispatch(setCredentials(data));

          if (process.env.NODE_ENV === 'production') {
            // analytics.track('User Login', { timestamp: new Date().toISOString() });
          }
        } catch (error: unknown) {
          const errorMessage = error instanceof Error ? error.message : 'Login failed';
          dispatch(setError(errorMessage));
          console.error('Login error:', error);
        }
      },
      invalidatesTags: ['Auth'],
    }),

    logout: build.mutation<void, void>({
      query: () => ({
        url: '/auth/logout',
        method: 'POST',
      }),
      async onQueryStarted(
        _: void, 
        { dispatch, queryFulfilled }: { dispatch: any; queryFulfilled: Promise<{ data: void }> }
      ) {
        try {
          await queryFulfilled;
          dispatch(clearCredentials());

          if ('util' in baseApi && typeof baseApi.util.resetApiState === 'function') {
            dispatch(baseApi.util.resetApiState());
          }
        } catch (error: unknown) {
          const errorMessage = error instanceof Error ? error.message : 'Logout failed';
          dispatch(setError(errorMessage));
          console.error('Logout error:', error);
        }
      },
      invalidatesTags: ['Auth'],
    }),
  }),
  overrideExisting: false,
});

export const { useLoginMutation, useLogoutMutation } = authApi;

