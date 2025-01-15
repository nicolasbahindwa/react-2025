//  auth.types

import { BaseQueryFn, FetchArgs, FetchBaseQueryError, MutationDefinition } from '@reduxjs/toolkit/query';

// Types for auth

export interface AuthUser {
    id: string;
    email: string;
    name: string;
    roles?: string[];
  }
  
  export interface LoginRequest {
    email: string;
    password: string;
  }
  
  export interface LoginResponse {
    user: AuthUser;
    accessToken: string;
    refreshToken: string;
    accessTokenExpiresIn: number; 
    refreshTokenExpiresIn: number;
  }
  
  export interface AuthTokens {
    accessToken: string;
    refreshToken: string;
    accessTokenExpiresIn: number;
    refreshTokenExpiresIn: number;
  }
  
  export interface ApiEndpointBuilder {
    mutation<ResultType, QueryArg = void>(
      options: {
        query: (arg: QueryArg) => FetchArgs;
        invalidatesTags?: any;
        onQueryStarted?: (
          arg: QueryArg,
          api: {
            dispatch: any;
            queryFulfilled: Promise<{ data: ResultType }>;
          }
        ) => Promise<void> | void;
      }
    ): MutationDefinition<
      QueryArg,
      BaseQueryFn<FetchArgs, ResultType, FetchBaseQueryError>,
      any,
      ResultType
    >;
  }
  
  export interface AuthState {
    user: AuthUser | null;
    tokens: AuthTokens;
    isAuthenticated: boolean;
    status: "idle" | "loading" | "succeeded" | "failed";
    error: string | null;
    lastLoginTime: string | null;
    sessionExpiresAt: string | null;
  }
  