import { baseApi } from '@/lib/baseApi';
import { EndpointBuilder } from '@reduxjs/toolkit/dist/query/endpointDefinitions';
import type { RegisterRequest, RegisterResponse } from '../Types/user.types';
import { setUser, setStatus, setError, clearUser } from '../slice/userAuthSlice';
import { Dispatch } from '@reduxjs/toolkit';

export const userApi = baseApi.injectEndpoints({
  endpoints: (build: EndpointBuilder<typeof baseApi.reducer, string, string>) => ({
    register: build.mutation<RegisterResponse, RegisterRequest>({
      query: (credentials: RegisterRequest) => ({
        url: '/auth/register',
        method: 'POST',
        body: credentials,
      }),
      async onQueryStarted(credentials: RegisterRequest, { dispatch, queryFulfilled }: { dispatch: Dispatch; queryFulfilled: Promise<{ data: RegisterResponse }> }) {
        dispatch(setStatus('loading'));
        try {
          const { data } = await queryFulfilled;
          dispatch(setUser(data));
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'Registration failed';
          dispatch(setError(errorMessage));
          console.error('Registration error:', error);
        }
      },
      invalidatesTags: ['Auth'],
    }),
    editUser: build.mutation<RegisterResponse, Partial<RegisterRequest>>({
      query: (userData: Partial<RegisterRequest>) => ({
        url: `/users/${userData.id}`,
        method: 'PATCH',
        body: userData,
      }),
      async onQueryStarted(userData: Partial<RegisterRequest>, { dispatch, queryFulfilled }: { dispatch: Dispatch; queryFulfilled: Promise<{ data: RegisterResponse }> }) {
        dispatch(setStatus('loading'));
        try {
          const { data } = await queryFulfilled;
          dispatch(setUser(data));
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'Failed to update user';
          dispatch(setError(errorMessage));
          console.error('Update user error:', error);
        }
      },
      invalidatesTags: ['Auth'],
    }),
    deleteUser: build.mutation<void, string>({
      query: (id: string) => ({
        url: `/users/${id}`,
        method: 'DELETE',
      }),
      async onQueryStarted(id: string, { dispatch, queryFulfilled }: { dispatch: Dispatch; queryFulfilled: Promise<void> }) {
        dispatch(setStatus('loading'));
        try {
          await queryFulfilled;
          dispatch(clearUser());
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'Failed to delete user';
          dispatch(setError(errorMessage));
          console.error('Delete user error:', error);
        }
      },
      invalidatesTags: ['Auth'],
    }),
  }),
  overrideExisting: false,
});

export const {
  useRegisterMutation,
  useEditUserMutation,
  useDeleteUserMutation,
} = userApi;

 