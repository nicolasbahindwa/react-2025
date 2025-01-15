import {
  createApi,
  fetchBaseQuery,
  FetchArgs,
} from "@reduxjs/toolkit/query/react";
import { RootState } from "@/store";
import {
  clearCredentials,
  updateAccessToken,
  setError,
} from "@/features/Auth/services/slice/authSlice";
import { ENV } from "@/config/environment";
import { AuthTokens } from "@/features/Auth/services/types/auth.types";
import { NavigateFunction } from "react-router-dom"; // Import NavigateFunction from React Router

// Token expiration buffer (1 minute)
const TOKEN_EXPIRY_BUFFER = 60 * 1000;

// Helper to check if token is about to expire
const isTokenExpiring = (expiresIn: number): boolean => {
  const expirationTime = new Date().getTime() + expiresIn * 1000;
  return expirationTime - new Date().getTime() <= TOKEN_EXPIRY_BUFFER;
};

const baseQuery = fetchBaseQuery({
  baseUrl: String(ENV.apiUrl).replace(/["']/g, "").replace(/\/$/, ""),
  credentials: "include",
  prepareHeaders: (headers, { getState }) => {
    headers.set("Content-Type", "application/json");
    const state = getState() as RootState;

    // Check if tokens exist before destructuring
    if (state.auth.tokens) {
      const { accessToken } = state.auth.tokens;
      if (accessToken) {
        headers.set("Authorization", `Bearer ${accessToken}`);
      }
    }

    return headers;
  },
});

// Semaphore to prevent multiple concurrent refresh attempts
let isRefreshing = false;
let refreshSubscribers: Array<(token: string) => void> = [];

// Helper to add new requests to queue
const addRefreshSubscriber = (callback: (token: string) => void) => {
  refreshSubscribers.push(callback);
};

// Helper to notify subscribers with new token
const onRefreshComplete = (token: string) => {
  refreshSubscribers.forEach((callback) => callback(token));
  refreshSubscribers = [];
};

// Pass navigate function from React Router
let navigate: NavigateFunction;

export const setNavigate = (navigateFunction: NavigateFunction) => {
  navigate = navigateFunction;
};

const baseQueryWithReauth = async (
  args: string | FetchArgs,
  api: any,
  extraOptions: {}
) => {
  const state = api.getState() as RootState;

  // Check if tokens exist before destructuring
  if (!state.auth.tokens) {
    handleLogout(api);
    return { error: { status: 401, data: "Unauthorized" } };
  }

  const { accessToken, refreshToken, accessTokenExpiresIn } = state.auth.tokens;

  // Check if token is about to expire before making the request
  if (accessToken && isTokenExpiring(accessTokenExpiresIn)) {
    if (!isRefreshing) {
      isRefreshing = true;
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
          const tokens = refreshResult.data as AuthTokens;
          api.dispatch(updateAccessToken(tokens));
          isRefreshing = false;
          onRefreshComplete(tokens.accessToken);
        } else {
          handleLogout(api);
          return refreshResult;
        }
      } catch (error) {
        handleLogout(api);
        return { error };
      }
    } else {
      // Wait for the refresh to complete
      const newToken = await new Promise<string>((resolve) => {
        addRefreshSubscriber(resolve);
      });
      if (typeof args === "string") {
        args = { url: args, method: "GET" };
      }
      args.headers = {
        ...args.headers,
        Authorization: `Bearer ${newToken}`,
      };
    }
  }

  // Make the actual request
  let result = await baseQuery(args, api, extraOptions);

  // Handle 401 errors
  if (result.error?.status === 401) {
    if (!isRefreshing) {
      isRefreshing = true;
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
          const tokens = refreshResult.data as AuthTokens;
          api.dispatch(updateAccessToken(tokens));
          isRefreshing = false;
          onRefreshComplete(tokens.accessToken);
          // Retry the original request
          result = await baseQuery(args, api, extraOptions);
        } else {
          handleLogout(api);
        }
      } catch (error) {
        handleLogout(api);
      }
    } else {
      // Wait for the refresh to complete
      const newToken = await new Promise<string>((resolve) => {
        addRefreshSubscriber(resolve);
      });
      if (typeof args === "string") {
        args = { url: args, method: "GET" };
      }
      args.headers = {
        ...args.headers,
        Authorization: `Bearer ${newToken}`,
      };
      result = await baseQuery(args, api, extraOptions);
    }
  }

  // Handle other error cases
  if (result.error) {
    const errorMessage =
      (result.error as any)?.data?.message ||
      (result.error as any)?.error ||
      "An error occurred";
    api.dispatch(setError(errorMessage));
  }

  return result;
};

// Handle user logout and redirect to login page
const handleLogout = (api: any) => {
  api.dispatch(clearCredentials());
  if (navigate) {
    navigate("/login"); // Use client-side navigation instead of page refresh
  } else {
    console.error("Navigate function is not set. Cannot redirect to login page.");
  }
};

export const baseApi = createApi({
  baseQuery: baseQueryWithReauth,
  endpoints: () => ({}),
  tagTypes: ["Auth", "User", "Profile"],
});