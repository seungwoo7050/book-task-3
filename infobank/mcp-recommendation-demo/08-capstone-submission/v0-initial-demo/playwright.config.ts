import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",
  timeout: 30_000,
  use: {
    baseURL: "http://127.0.0.1:3000",
    trace: "retain-on-failure"
  },
  webServer: [
    {
      command:
        "pnpm --filter @study1-v0/node dev:test",
      cwd: ".",
      port: 3100,
      reuseExistingServer: true,
      env: {
        DATABASE_URL:
          process.env.DATABASE_URL ?? "postgres://postgres:postgres@127.0.0.1:5540/study1_v0",
        PORT: "3100"
      }
    },
    {
      command:
        "pnpm --filter @study1-v0/react dev",
      cwd: ".",
      port: 3000,
      reuseExistingServer: true,
      env: {
        NEXT_PUBLIC_API_BASE_URL:
          process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:3100"
      }
    }
  ]
});
