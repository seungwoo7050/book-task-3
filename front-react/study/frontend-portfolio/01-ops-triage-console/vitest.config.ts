import path from "node:path";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./next/src"),
    },
  },
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: "./next/tests/setup.ts",
    include: [
      "./next/tests/unit/**/*.test.ts",
      "./next/tests/integration/**/*.test.tsx",
    ],
    css: true,
  },
});

