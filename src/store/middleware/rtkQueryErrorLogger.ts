import { isRejectedWithValue } from '@reduxjs/toolkit';
import type { Middleware } from 'redux';

/**
 * Middleware for logging RTK Query errors
 */
const rtkQueryErrorLogger: Middleware = () => (next) => (action) => {
  if (isRejectedWithValue(action)) {
    console.error('RTK Query error:', action.payload);
    // You could also send to an error reporting service here
  }
  return next(action);
};

export default rtkQueryErrorLogger;