// import { baseApi } from '@/lib/baseApi';
// import { LoginRequest, LoginResponse } from '../Types';
// import { setCredentials, clearCredentials, setError, setLoading } from '../slice/authSlice';
// import { EndpointBuilder } from '@reduxjs/toolkit/dist/query/endpointDefinitions';
// import { Dispatch } from '@reduxjs/toolkit';

// export const authApi = baseApi.injectEndpoints({
//   endpoints: (build: EndpointBuilder<typeof baseApi.reducer, string, string>) => ({
     
//     login: build.mutation<LoginResponse, LoginRequest>({
//       query: (credentials: LoginRequest) => ({
//         url: '/auth/login',
//         method: 'POST',
//         body: credentials,
//       }),
//       async onQueryStarted(_: void, { dispatch, queryFulfilled }: { dispatch: Dispatch; queryFulfilled: Promise<any> }) {
//         dispatch(setLoading());
//         try {
//           const { data } = await queryFulfilled;
//           dispatch(setCredentials(data));
//         } catch (error) {
//           dispatch(setError(error instanceof Error ? error.message : 'Login failed'));
//         }
//       },
//       invalidatesTags: ['Auth'],
//     }),
//     logout: build.mutation<void, void>({
//       query: () => ({
//         url: '/auth/logout',
//         method: 'POST',
//       }),
//       async onQueryStarted(_: void, { dispatch, queryFulfilled }: { dispatch: Dispatch; queryFulfilled: Promise<any> }) {
//         try {
//           await queryFulfilled;
//           dispatch(clearCredentials());
//         } catch (error) {
//           dispatch(setError(error instanceof Error ? error.message : 'Logout failed'));
//         }
//       },
//       invalidatesTags: ['Auth'],
//     }),
//   }),
//   overrideExisting: false,
// });

// export const {
//   useLoginMutation,
//   useLogoutMutation,
// } = authApi;


import { baseApi } from "@/lib/baseApi";
import { LoginRequest, LoginResponse } from "../../types/auth.types";
import {
  setCredentials,
  clearCredentials,
  setError,
  setLoading,
} from "../slice/authSlice";
import { EndpointBuilder } from "@reduxjs/toolkit/dist/query/endpointDefinitions";

export const authApi = baseApi.injectEndpoints({
  endpoints: (build) => ({
    login: build.mutation<LoginResponse, LoginRequest>({
      query: (credentials) => ({
        url: "/auth/login",
        method: "POST",
        body: credentials,
      }),
      async onQueryStarted(_, { dispatch, queryFulfilled }) {
        dispatch(setLoading());
        try {
          const { data } = await queryFulfilled;
          dispatch(setCredentials(data));

          // Optional: Track successful login
          if (process.env.NODE_ENV === "production") {
            // analytics.track('User Login', { timestamp: new Date() });
          }
        } catch (error) {
          const errorMessage =
            error instanceof Error ? error.message : "Login failed";
          dispatch(setError(errorMessage));
          console.error("Login error:", error);
        }
      },
      invalidatesTags: ["Auth"],
    }),
    logout: build.mutation<void, void>({
      query: () => ({
        url: "/auth/logout",
        method: "POST",
      }),
      async onQueryStarted(_, { dispatch, queryFulfilled }) {
        try {
          await queryFulfilled;
          dispatch(clearCredentials());

          // Clear any cached data
          dispatch(baseApi.util.resetApiState());
        } catch (error) {
          const errorMessage =
            error instanceof Error ? error.message : "Logout failed";
          dispatch(setError(errorMessage));
          console.error("Logout error:", error);
        }
      },
      invalidatesTags: ["Auth"],
    }),
  }),
  overrideExisting: false,
});

export const { useLoginMutation, useLogoutMutation } = authApi;