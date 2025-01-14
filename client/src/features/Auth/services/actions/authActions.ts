import { baseApi } from '@/lib/baseApi';
import { LoginRequest, LoginResponse } from '../Types';
import { setCredentials, clearCredentials, setError, setLoading } from '../slice/authSlice';
import { EndpointBuilder } from '@reduxjs/toolkit/dist/query/endpointDefinitions';
import { Dispatch } from '@reduxjs/toolkit';

export const authApi = baseApi.injectEndpoints({
  endpoints: (build: EndpointBuilder<typeof baseApi.reducer, string, string>) => ({
     
    login: build.mutation<LoginResponse, LoginRequest>({
      query: (credentials: LoginRequest) => ({
        url: '/auth/login',
        method: 'POST',
        body: credentials,
      }),
      async onQueryStarted(_: void, { dispatch, queryFulfilled }: { dispatch: Dispatch; queryFulfilled: Promise<any> }) {
        dispatch(setLoading());
        try {
          const { data } = await queryFulfilled;
          dispatch(setCredentials(data));
        } catch (error) {
          dispatch(setError(error instanceof Error ? error.message : 'Login failed'));
        }
      },
      invalidatesTags: ['Auth'],
    }),
    logout: build.mutation<void, void>({
      query: () => ({
        url: '/auth/logout',
        method: 'POST',
      }),
      async onQueryStarted(_: void, { dispatch, queryFulfilled }: { dispatch: Dispatch; queryFulfilled: Promise<any> }) {
        try {
          await queryFulfilled;
          dispatch(clearCredentials());
        } catch (error) {
          dispatch(setError(error instanceof Error ? error.message : 'Logout failed'));
        }
      },
      invalidatesTags: ['Auth'],
    }),
  }),
  overrideExisting: false,
});

export const {
  useLoginMutation,
  useLogoutMutation,
} = authApi;