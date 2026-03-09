import { catalogSeeds } from "@study1-v3/shared";
import type { FastifyInstance } from "fastify";
import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { buildApp } from "../src/app.js";
import { stopBoss, startJobWorker } from "../src/services/job-service.js";

let app: FastifyInstance;
const integrationDescribe = process.env.RUN_DB_TESTS === "1" ? describe : describe.skip;

function extractCookie(response: Awaited<ReturnType<FastifyInstance["inject"]>>) {
  const header = response.headers["set-cookie"];
  const cookie = Array.isArray(header) ? header[0] : header;
  if (!cookie) {
    throw new Error("session cookie was not returned");
  }
  const [token] = cookie.split(";");
  if (!token) {
    throw new Error("session token was not returned");
  }
  return token;
}

async function login(email: string, password: string) {
  const response = await app.inject({
    method: "POST",
    url: "/api/auth/login",
    payload: { email, password }
  });

  expect(response.statusCode).toBe(200);
  return extractCookie(response);
}

async function waitForJob(cookie: string, jobId: string) {
  for (let attempt = 0; attempt < 40; attempt += 1) {
    const response = await app.inject({
      method: "GET",
      url: `/api/jobs/${jobId}`,
      headers: { cookie }
    });

    expect(response.statusCode).toBe(200);
    const body = response.json() as { item: { status: string; errorSummary: string | null } };
    if (body.item.status === "completed" || body.item.status === "failed") {
      return body.item;
    }

    await new Promise((resolve) => setTimeout(resolve, 500));
  }

  throw new Error(`job ${jobId} did not finish in time`);
}

integrationDescribe("route contracts", () => {
  beforeAll(async () => {
    app = await buildApp();
    await startJobWorker();
  });

  afterAll(async () => {
    await app.close();
    await stopBoss();
  });

  it("enforces auth and role guards and records owner mutations", async () => {
    const seedCatalog = catalogSeeds[0];
    if (!seedCatalog) {
      throw new Error("catalogSeeds is empty");
    }

    const anonymousResponse = await app.inject({
      method: "GET",
      url: "/api/catalog"
    });
    expect(anonymousResponse.statusCode).toBe(401);

    const viewerCookie = await login("viewer@study1.local", "Viewer123!");
    const viewerMutation = await app.inject({
      method: "POST",
      url: "/api/catalog",
      headers: { cookie: viewerCookie },
      payload: seedCatalog
    });
    expect(viewerMutation.statusCode).toBe(403);

    const ownerCookie = await login("owner@study1.local", "ChangeMe123!");
    const usersResponse = await app.inject({
      method: "GET",
      url: "/api/users",
      headers: { cookie: ownerCookie }
    });
    expect(usersResponse.statusCode).toBe(200);
    const usersBody = usersResponse.json() as { items: Array<{ email: string }> };
    expect(usersBody.items.some((item) => item.email === "owner@study1.local")).toBe(true);

    const uniqueUserEmail = `integration-${Date.now()}@study1.local`;
    const createUserResponse = await app.inject({
      method: "POST",
      url: "/api/users",
      headers: { cookie: ownerCookie },
      payload: {
        email: uniqueUserEmail,
        name: "Integration Operator",
        role: "operator",
        password: "Operator123!"
      }
    });
    expect(createUserResponse.statusCode).toBe(200);

    const settingsResponse = await app.inject({
      method: "PUT",
      url: "/api/settings",
      headers: { cookie: ownerCookie },
      payload: {
        workspaceName: "Study1 OSS Team",
        defaultLocale: "ko-KR",
        defaultClientVersion: "1.2.0",
        evalMinTop3Recall: 0.9,
        compareMinUplift: 0.02
      }
    });
    expect(settingsResponse.statusCode).toBe(200);

    const auditResponse = await app.inject({
      method: "GET",
      url: "/api/audit-logs",
      headers: { cookie: ownerCookie }
    });
    expect(auditResponse.statusCode).toBe(200);
    const auditBody = auditResponse.json() as { items: Array<{ action: string; detailKo: string }> };
    expect(auditBody.items.some((item) => item.action === "auth.login")).toBe(true);
    expect(auditBody.items.some((item) => item.action === "user.create")).toBe(true);
    expect(auditBody.items.some((item) => item.action === "settings.update")).toBe(true);
  });

  it(
    "exports and imports bundles and completes queued jobs",
    async () => {
      const operatorCookie = await login("operator@study1.local", "Operator123!");

      const exportResponse = await app.inject({
        method: "GET",
        url: "/api/catalog/export",
        headers: { cookie: operatorCookie }
      });
      expect(exportResponse.statusCode).toBe(200);
      const exportBody = exportResponse.json() as {
        item: {
          catalogEntries: Array<{ id: string; slug: string; name: string }>;
          evalCases: unknown[];
          releaseCandidates: unknown[];
        };
      };
      expect(exportBody.item.catalogEntries.length).toBeGreaterThanOrEqual(12);

      const importBundle = {
        ...exportBody.item,
        catalogEntries: [
          ...exportBody.item.catalogEntries,
          {
            ...exportBody.item.catalogEntries[0],
            id: `oss-import-${Date.now()}`,
            slug: `oss-import-${Date.now()}`,
            name: "OSS Import Sample"
          }
        ]
      };
      const importResponse = await app.inject({
        method: "POST",
        url: "/api/catalog/import",
        headers: { cookie: operatorCookie },
        payload: importBundle
      });
      expect(importResponse.statusCode).toBe(200);

      const evalEnqueue = await app.inject({
        method: "POST",
        url: "/api/jobs/eval",
        headers: { cookie: operatorCookie }
      });
      expect(evalEnqueue.statusCode).toBe(200);
      const evalJobId = (evalEnqueue.json() as { jobId?: string }).jobId;
      expect(evalJobId).toBeTruthy();
      const evalResult = await waitForJob(operatorCookie, evalJobId!);
      expect(evalResult.status).toBe("completed");

      const compareEnqueue = await app.inject({
        method: "POST",
        url: "/api/jobs/compare",
        headers: { cookie: operatorCookie },
        payload: { experimentId: "exp-release-signal" }
      });
      const compareJobId = (compareEnqueue.json() as { jobId?: string }).jobId;
      expect(compareJobId).toBeTruthy();
      const compareResult = await waitForJob(operatorCookie, compareJobId!);
      expect(compareResult.status).toBe("completed");

      const compatibilityEnqueue = await app.inject({
        method: "POST",
        url: "/api/jobs/compatibility",
        headers: { cookie: operatorCookie },
        payload: { releaseCandidateId: "rc-release-check-bot-1-5-0" }
      });
      const compatibilityJobId = (compatibilityEnqueue.json() as { jobId?: string }).jobId;
      expect(compatibilityJobId).toBeTruthy();
      const compatibilityResult = await waitForJob(operatorCookie, compatibilityJobId!);
      expect(compatibilityResult.status).toBe("completed");

      const gateEnqueue = await app.inject({
        method: "POST",
        url: "/api/jobs/release-gate",
        headers: { cookie: operatorCookie },
        payload: { releaseCandidateId: "rc-release-check-bot-1-5-0" }
      });
      const gateJobId = (gateEnqueue.json() as { jobId?: string }).jobId;
      expect(gateJobId).toBeTruthy();
      const gateResult = await waitForJob(operatorCookie, gateJobId!);
      expect(gateResult.status).toBe("completed");

      const artifactEnqueue = await app.inject({
        method: "POST",
        url: "/api/jobs/artifact-export",
        headers: { cookie: operatorCookie },
        payload: { releaseCandidateId: "rc-release-check-bot-1-5-0" }
      });
      const artifactJobId = (artifactEnqueue.json() as { jobId?: string }).jobId;
      expect(artifactJobId).toBeTruthy();
      const artifactResult = await waitForJob(operatorCookie, artifactJobId!);
      expect(artifactResult.status).toBe("completed");

      const gateLatestResponse = await app.inject({
        method: "GET",
        url: "/api/release-gate/latest",
        headers: { cookie: operatorCookie }
      });
      expect(gateLatestResponse.statusCode).toBe(200);
      const gateLatestBody = gateLatestResponse.json() as {
        latest: { passed: boolean; metrics: { top3Recall: number; uplift: number } } | null;
      };
      expect(gateLatestBody.latest?.passed).toBe(true);
      expect(gateLatestBody.latest?.metrics.top3Recall ?? 0).toBeGreaterThanOrEqual(0.9);
      expect(gateLatestBody.latest?.metrics.uplift ?? 0).toBeGreaterThanOrEqual(0.02);

      const artifactLatestResponse = await app.inject({
        method: "GET",
        url: "/api/submission/latest",
        headers: { cookie: operatorCookie }
      });
      expect(artifactLatestResponse.statusCode).toBe(200);
      const artifactLatestBody = artifactLatestResponse.json() as {
        latest: { content: string } | null;
      };
      expect(artifactLatestBody.latest?.content).toContain("## Release Notes");
    },
    20_000
  );
});
