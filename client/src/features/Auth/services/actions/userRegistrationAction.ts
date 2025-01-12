import { baseApi } from '@/lib/baseApi';
import { EndpointBuilder } from '@reduxjs/toolkit/dist/query/endpointDefinitions';
import type { RegisterRequest, RegisterResponse } from '../Types';
import { setUser, setError, setLoading } from '../slice/userAuthSlice';
import { Dispatch } from '@reduxjs/toolkit';

export const authApi = baseApi.injectEndpoints({
  endpoints: (build: EndpointBuilder<typeof baseApi.reducer, string, string>) => ({
    register: build.mutation<RegisterResponse, RegisterRequest>({
      query: (credentials: RegisterRequest) => ({
        url: '/auth/register',
        method: 'POST',
        body: credentials,
      }),
      async onQueryStarted(_: void, { dispatch, queryFulfilled }: { dispatch: Dispatch; queryFulfilled: Promise<any> }) {
        console.log("*** ------------------- starting")
        dispatch(setLoading(true)); // Set loading to true at the start
        try {
          const { data } = await queryFulfilled;
          dispatch(setUser(data)); // Dispatch setUser with the correct payload
        } catch (error: unknown) {
          dispatch(setError(error instanceof Error ? error.message : 'Registration failed')); // Proper error handling
        } finally {
          dispatch(setLoading(false)); // Ensure loading is false after completion
        }
      },
      invalidatesTags: ['Auth'],
    }),
  }),
  overrideExisting: false,
});

export const { useRegisterMutation } = authApi;