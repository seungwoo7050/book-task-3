import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "jsdom",
    include: ["vanilla/tests/**/*.test.ts"],
    globals: true,
  },
});
