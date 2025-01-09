import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import { fileURLToPath } from 'url';
import path from 'path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig(({ mode }) => {
  // Load env files from parent directory with empty prefix to load all variables
  const env = loadEnv(mode, path.resolve(__dirname, '..'), '');

  return {
    plugins: [react()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },
    "compilerOptions": {
      "strict": true,
      "noImplicitAny": true,
      "strictFunctionTypes": true,
      "skipLibCheck": true,
      "esModuleInterop": true,
      "baseUrl": ".",
      "paths": { "@/*": ["src/*"] }
    },
    envDir: path.resolve(__dirname, '..'), // Point to parent directory for .env
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: `@use "@/assets/styles/themes/_variables.scss" as *;`,
        },
      },
      devSourcemap: true,
      modules: {
        generateScopedName: mode === 'production' ? '[hash:base64:5]' : '[name]__[local]',
      },
    },
    build: {
      outDir: 'dist',
      cssCodeSplit: true,
      minify: true,
      rollupOptions: {
        output: {
          assetFileNames: 'styles/[name].[hash].css',
        },
      },
    },
    server: {
      watch: {
        usePolling: true,
        interval: 100,
      },
      port: parseInt(env.APP_PORT) || 5000,
    },
    define: {
      // This line maps all the environment variables automatically
      'import.meta.env': {
        ...Object.fromEntries(
          Object.entries(env).map(([key, val]) => [key, JSON.stringify(val)])
        )
      }
    },
  };
});
