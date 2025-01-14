// import { createApi, fetchBaseQuery, FetchArgs, FetchBaseQueryError } from '@reduxjs/toolkit/query/react';
// import { RootState } from '@/store';
// import { clearCredentials } from '@/features/Auth/services/slice/authSlice';
// import { ENV } from '@/config/environment';

// const baseQuery = fetchBaseQuery({
//   baseUrl: String(ENV.apiUrl).replace(/["']/g, "").replace(/\/$/, ""),
//   credentials: "include",
//   prepareHeaders: (headers, { getState }) => {
//     headers.set("Content-Type", "application/json");
//     const token = (getState() as RootState).auth.user?.token;
//     if (token) {
//       headers.set("Authorization", `Bearer ${token}`);
//     }

//     return headers;
//   },
// });

// const baseQueryWithReauth = async (args: string | FetchArgs, api: any, extraOptions: {}) => {
//   const result = await baseQuery(args, api, extraOptions);
  
//   if (result.error?.status === 401) {
//     api.dispatch(clearCredentials());
//     window.location.href = '/login';
//   }
  
//   return result;
// };

// export const baseApi = createApi({
//   baseQuery: baseQueryWithReauth,
//   endpoints: () => ({}),
//   tagTypes: ['Auth'],
// });


import {
  createApi,
  fetchBaseQuery,
  FetchArgs,
  FetchBaseQueryError,
} from "@reduxjs/toolkit/query/react";
import { RootState } from "@/store";
import {
  clearCredentials,
  updateAccessToken,
} from "@/features/Auth/services/slice/authSlice";
import { ENV } from "@/config/environment";

const baseQuery = fetchBaseQuery({
  baseUrl: String(ENV.apiUrl).replace(/["']/g, "").replace(/\/$/, ""),
  credentials: "include",
  prepareHeaders: (headers, { getState }) => {
    headers.set("Content-Type", "application/json");
    const token = (getState() as RootState).auth.tokens.accessToken;
    if (token) {
      headers.set("Authorization", `Bearer ${token}`);
    }
    return headers;
  },
});

const baseQueryWithReauth = async (
  args: string | FetchArgs,
  api: any,
  extraOptions: {}
) => {
  let result = await baseQuery(args, api, extraOptions);

  if (result.error?.status === 401) {
    // Try to refresh the token
    const refreshToken = (api.getState() as RootState).auth.tokens.refreshToken;

    if (refreshToken) {
      try {
        const refreshResult = await baseQuery(
          {
            url: "/auth/refresh",
            method: "POST",
            body: { refreshToken },
          },
          api,
          extraOptions
        );

        if (refreshResult.data) {
          // Update the token
          api.dispatch(updateAccessToken(refreshResult.data));
          // Retry the original request
          result = await baseQuery(args, api, extraOptions);
        } else {
          // If refresh fails, log out
          api.dispatch(clearCredentials());
          window.location.href = "/login";
        }
      } catch {
        api.dispatch(clearCredentials());
        window.location.href = "/login";
      }
    } else {
      api.dispatch(clearCredentials());
      window.location.href = "/login";
    }
  }

  return result;
};

export const baseApi = createApi({
  baseQuery: baseQueryWithReauth,
  endpoints: () => ({}),
  tagTypes: ["Auth", "User", "Profile"],
});