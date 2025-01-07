import { StoreEnhancer, compose } from 'redux';
import type { ConfigureStoreOptions, EnhancedStore } from '@reduxjs/toolkit';
import monitorReducerEnhancer from './monitorReducer';
import loggerEnhancer from './logger';

type EnhancerFunction = ConfigureStoreOptions['enhancers'];

export const getEnhancers: EnhancerFunction = (getDefaultEnhancers) => {
  const enhancers: StoreEnhancer[] = [];

  if (process.env.NODE_ENV === 'development') {
    enhancers.push(monitorReducerEnhancer);
    enhancers.push(loggerEnhancer);
  }

  return getDefaultEnhancers().concat(enhancers);
};