import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { FormRegister, RegisterResponse } from '@/features/Auth/types/auth.types';

export const authApi = createApi({
  reducerPath: 'authApi',
  baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
  endpoints: (builder) => ({
    register: builder.mutation<RegisterResponse, FormRegister>({
      query: (credentials) => ({
        url: '/auth/register',
        method: 'POST',
        body: credentials,
      }),
    }),
  }),
});

export const { useRegisterMutation } = authApi;