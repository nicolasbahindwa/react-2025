 


// src/store/api/authApi.ts
import { baseApi } from '@/lib/baseApi';
import { EndpointBuilder } from '@reduxjs/toolkit/dist/query/endpointDefinitions';
import type { RegisterRequest, RegisterResponse } from '../Types';
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
      async onQueryStarted(_: void, { dispatch, queryFulfilled }: { dispatch: Dispatch; queryFulfilled: Promise<any> }) {
        dispatch(setStatus('loading'));
        try {
          const { data } = await queryFulfilled;
          dispatch(setUser(data));
        } catch (error) {
          dispatch(setError(error instanceof Error ? error.message : 'Registration failed'));
        }
      },
      invalidatesTags: ['Auth'],
    }),
    editUser: build.mutation<RegisterResponse, Partial<RegisterRequest>>({
      
      query: (userData: RegisterRequest) => ({
        url: `/users/${userData.id}`,
        method: 'PATCH',
        body: userData,
      }),
      async onQueryStarted(_: void, { dispatch, queryFulfilled }: { dispatch: Dispatch; queryFulfilled: Promise<any> }) {
        dispatch(setStatus('loading'));
        try {
          const { data } = await queryFulfilled;
          dispatch(setUser(data));
        } catch (error) {
          dispatch(setError(error instanceof Error ? error.message : 'Failed to update user'));
        }
      },
      invalidatesTags: ['Auth'],
    }),
    deleteUser: build.mutation<void, string>({
      query: (id:string) => ({
        url: `/users/${id}`,
        method: 'DELETE',
      }),
      async onQueryStarted(_: void, { dispatch, queryFulfilled }: { dispatch: Dispatch; queryFulfilled: Promise<any> }) {
        dispatch(setStatus('loading'));
        try {
          await queryFulfilled;
          dispatch(clearUser());
        } catch (error) {
          dispatch(setError(error instanceof Error ? error.message : 'Failed to delete user'));
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
