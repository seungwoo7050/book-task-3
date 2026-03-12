import { describe, expect, it } from "vitest";

import { loadRuntimeConfig } from "../../src/runtime/runtime-config";

describe("loadRuntimeConfig", () => {
  it("uses documented defaults", () => {
    expect(loadRuntimeConfig({})).toEqual({
      appName: "production-readiness-app",
      environment: "development",
      port: 3000,
      ready: true,
      logLevel: "info",
    });
  });

  it("parses explicit values", () => {
    expect(
      loadRuntimeConfig({
        APP_NAME: "backend-study-app",
        NODE_ENV: "test",
        PORT: "3100",
        READY: "false",
        LOG_LEVEL: "debug",
      }),
    ).toEqual({
      appName: "backend-study-app",
      environment: "test",
      port: 3100,
      ready: false,
      logLevel: "debug",
    });
  });

  it("fails fast for invalid ports", () => {
    expect(() => loadRuntimeConfig({ PORT: "not-a-number" })).toThrow(
      "PORT must be a positive integer",
    );
  });
});
