import { INestApplication } from "@nestjs/common";
import { Test } from "@nestjs/testing";
import request from "supertest";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { AppModule } from "../../src/app.module";

type EnvPatch = Record<string, string | undefined>;

async function createTestApp(envPatch: EnvPatch): Promise<INestApplication> {
  process.env = { ...process.env, ...envPatch };

  const moduleRef = await Test.createTestingModule({
    imports: [AppModule],
  }).compile();

  const app = moduleRef.createNestApplication();
  await app.init();

  return app;
}

describe("production readiness e2e", () => {
  const stdoutSpy = vi.spyOn(process.stdout, "write").mockImplementation(() => true);

  beforeEach(() => {
    stdoutSpy.mockClear();
  });

  afterEach(() => {
    delete process.env.APP_NAME;
    delete process.env.READY;
    delete process.env.PORT;
    delete process.env.LOG_LEVEL;
    delete process.env.NODE_ENV;
  });

  it("returns health data", async () => {
    const app = await createTestApp({
      APP_NAME: "backend-study-app",
      READY: "true",
      LOG_LEVEL: "info",
      NODE_ENV: "test",
    });

    await request(app.getHttpServer())
      .get("/health")
      .expect(200)
      .expect(({ body }) => {
        expect(body.status).toBe("ok");
        expect(body.appName).toBe("backend-study-app");
        expect(body.environment).toBe("test");
      });

    await app.close();
  });

  it("returns 503 when readiness is disabled", async () => {
    const app = await createTestApp({
      APP_NAME: "backend-study-app",
      READY: "false",
      LOG_LEVEL: "warn",
      NODE_ENV: "test",
    });

    await request(app.getHttpServer())
      .get("/ready")
      .expect(503)
      .expect(({ body }) => {
        expect(body.status).toBe("not-ready");
      });

    expect(stdoutSpy).toHaveBeenCalled();
    await app.close();
  });
});
