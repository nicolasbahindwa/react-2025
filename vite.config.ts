import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { fileURLToPath } from "url";
import path from "path";
import dotenv from 'dotenv';

dotenv.config();
const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  plugins: [react()],
  resolve: {
    main: './src/main.tsx',
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  define: {
    'process.env': {
        REACT_APP_API_BASE_URL: JSON.stringify(process.env.REACT_APP_API_BASE_URL),
        NODE_ENV: JSON.stringify(process.env.NODE_ENV || 'development'),
    },
},
   
});
