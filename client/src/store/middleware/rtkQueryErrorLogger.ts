import { isRejectedWithValue, Middleware } from "@reduxjs/toolkit";

interface EndpointMetaData {
  arg: {
    endpointName?: string;
    originalArgs?: any;
  };
  requestId: string;
  startTime: number;
}

interface ErrorPayload {
  status?: number;
  data?: any;
  error?: string;
}

// Simple logging utility
const logError = (errorPayload: any) => {
  console.error('RTK Query Error:', errorPayload);
  // You can also send the error to a logging service here (e.g., Sentry, LogRocket).
};

const rtkQueryErrorLogger: Middleware = () => (next) => (action) => {
  if (isRejectedWithValue(action)) {
    const meta = action.meta as Partial<EndpointMetaData>; // Use Partial to allow missing properties
    const payload = action.payload as ErrorPayload;

    // Check if startTime exists and calculate the duration
    const duration = meta.startTime ? Date.now() - meta.startTime : 0;

    // Extract endpoint details
    const endpointName = meta.arg?.endpointName || "unknown";
    const endpointUrl = meta.arg?.originalArgs?.url || "unknown"; // Add URL if available
    const endpointMethod = meta.arg?.originalArgs?.method || "unknown"; // Add HTTP method if available

    const errorPayload = {
      timestamp: new Date().toISOString(),
      endpoint: {
        name: endpointName,
        url: endpointUrl,
        method: endpointMethod,
      },
      requestId: meta.requestId || "unknown",
      status: payload.status,
      error: payload.error,
      data: payload.data,
      duration,
      originalArgs: meta.arg?.originalArgs,
      environment: process.env.NODE_ENV,
    };

    // Log the error using the logging utility
    logError(errorPayload);
  }

  return next(action);
};

export default rtkQueryErrorLogger;