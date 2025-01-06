// import { defineConfig } from "vite";
// import react from "@vitejs/plugin-react";
// import { fileURLToPath } from "url";
// import path from "path";
// import dotenv from 'dotenv';

// dotenv.config();
// const __dirname = path.dirname(fileURLToPath(import.meta.url));

// export default defineConfig({
//   plugins: [react()],
//   resolve: {
//     main: './src/main.tsx',
//     alias: {
//       "@": path.resolve(__dirname, "./src"),
//     },
//   },
//   define: {
//     'process.env': {
//         REACT_APP_API_BASE_URL: JSON.stringify(process.env.REACT_APP_API_BASE_URL),
//         NODE_ENV: JSON.stringify(process.env.NODE_ENV || 'development'),
//     },
// },
   
// });

// import { defineConfig } from "vite";
// import react from "@vitejs/plugin-react";
// import { fileURLToPath } from "url";
// import path from "path";
// import dotenv from "dotenv";

// dotenv.config();
// const __dirname = path.dirname(fileURLToPath(import.meta.url));

// export default defineConfig({
//   plugins: [react()],
//   resolve: {
//     alias: {
//       "@": path.resolve(__dirname, "./src"),
//     },
//   },
//   css: {
//     preprocessorOptions: {
//       scss: {
//         additionalData: `@use "@/assets/styles/themes/_variables.scss" as *;`, // Using "as *" to avoid conflicts
//       },
//     },
//   },
//   build: {
//     cssCodeSplit: true, // Ensures CSS is extracted
//     rollupOptions: {
//       input: path.resolve(__dirname, "src/assets/styles/main.scss"), // Correct path for the SCSS entry
//       output: {
//         assetFileNames: "src/assets/styles/[name].[hash].css", // Correct output path
//       },
//     },
//   },
//   define: {
//     "process.env": process.env,
//   },
// });



import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { fileURLToPath } from "url";
import path from "path";
import dotenv from "dotenv";

dotenv.config();
const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@use "@/assets/styles/themes/_variables.scss" as *;`,
      },
    },
    devSourcemap: true,
    modules: {
      generateScopedName:
        process.env.NODE_ENV === "production"
          ? "[hash:base64:5]"
          : "[name]__[local]",
    },
  },
  build: {
    outDir: "dist", // Ensure this points to your build directory
    cssCodeSplit: true,
    minify: true,
    rollupOptions: {
      output: {
        assetFileNames: "styles/[name].[hash].css", // Use hash in CSS filenames
      },
    },
  },
  server: {
    watch: {
      usePolling: true,
      interval: 100, // Optional polling interval in milliseconds
    },
  },
  define: {
    "process.env": process.env,
  },
});
