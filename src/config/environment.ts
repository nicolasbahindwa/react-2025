const requireEnvVar = (name: string): string => {
    const value = process.env[name];
    if (!value) {
        throw new Error(`Missing required environment variable: ${name}`);
    }
    return value;
};

export const ENV = {
    

    API_BASE_URL: requireEnvVar('REACT_APP_API_BASE_URL'),
    NODE_ENV: process.env.NODE_ENV || 'development',
    
} as const;
