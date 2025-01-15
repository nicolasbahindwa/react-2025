import { StoreEnhancer, Tuple } from '@reduxjs/toolkit';
import type { ConfigureStoreOptions } from '@reduxjs/toolkit';
import monitorReducerEnhancer from './monitorReducer';
import loggerEnhancer from './logger';

// Explicitly type the getEnhancers function
export const getEnhancers: ConfigureStoreOptions['enhancers'] = (getDefaultEnhancers) => {
  // Call the getDefaultEnhancers function to get the default enhancers as a Tuple
  const defaultEnhancers = getDefaultEnhancers();

  // Create a new Tuple with the default enhancers
  const enhancers = new Tuple(...defaultEnhancers);

  if (process.env.NODE_ENV === 'development') {
    // Add custom enhancers in development mode
    enhancers.push(monitorReducerEnhancer as StoreEnhancer);
    enhancers.push(loggerEnhancer as StoreEnhancer);
  }

  return enhancers;
};