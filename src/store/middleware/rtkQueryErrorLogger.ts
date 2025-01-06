import { isRejectedWithValue, Middleware } from "@reduxjs/toolkit";
import { logError } from "@/utils/logger"; // Import logError from logger

interface EndpointMetaData {
  arg: {
    endpointName?: string;
  };
  requestId: string;
}

interface ErrorPayload {
  status?: number;
  data?: any;
  error?: string;
}

const rtkQueryErrorLogger: Middleware = () => (next) => (action) => {
  if (isRejectedWithValue(action)) {
    const meta = action.meta as EndpointMetaData;
    const payload = action.payload as ErrorPayload;

    const errorPayload = {
      timestamp: new Date().toISOString(),
      endpointName: meta.arg?.endpointName || "unknown",
      requestId: meta.requestId,
      status: payload.status,
      error: payload.error,
      data: payload.data,
    };

    // Log the error
    logError(errorPayload);
  }

  return next(action);
};

export default rtkQueryErrorLogger;
