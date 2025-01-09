const getEnvVar = (name: string, fallback?: string): string => {
    const value = import.meta.env[name];
    if (!value && fallback === undefined) {
      throw new Error(`Missing required environment variable: ${name}`);
    }
    return value || fallback || '';
  };
  
  // Map environment variables from root .env
  export const ENV = {
    apiUrl: getEnvVar('VITE_API_URL'),
    nodeEnv: getEnvVar('VITE_NODE_ENV'),
    appPort: getEnvVar('VITE_APP_PORT'),
    // databaseUrl: getEnvVar('VITE_DATABASE_URL'),
    secretKey: getEnvVar('VITE_SECRET_KEY'),
    // Add other variables as needed
  } as const;
  
  // For debugging - remove in production
  if (import.meta.env.DEV) {
    console.log('Environment loaded:', {
      apiUrl: ENV.apiUrl,
      nodeEnv: ENV.nodeEnv,
      appPort: ENV.appPort,
      // Add other variables you want to check
    });
  }

  export type Environment = typeof ENV;