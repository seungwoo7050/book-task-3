import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",
  timeout: 30_000,
  use: {
    baseURL: "http://127.0.0.1:3003",
    trace: "retain-on-failure"
  },
  webServer: [
    {
      command:
        "pnpm --filter @study1-v3/node dev:test",
      cwd: ".",
      port: 3103,
      reuseExistingServer: true,
      env: {
        DATABASE_URL:
          process.env.DATABASE_URL ?? "postgres://postgres:postgres@127.0.0.1:5543/study1_v3",
        PORT: "3103",
        APP_BASE_URL: process.env.APP_BASE_URL ?? "http://127.0.0.1:3003",
        INLINE_JOB_WORKER: "true"
      }
    },
    {
      command:
        "pnpm --filter @study1-v3/react dev",
      cwd: ".",
      port: 3003,
      reuseExistingServer: true,
      env: {
        NEXT_PUBLIC_API_BASE_URL:
          process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:3103"
      }
    }
  ]
});
