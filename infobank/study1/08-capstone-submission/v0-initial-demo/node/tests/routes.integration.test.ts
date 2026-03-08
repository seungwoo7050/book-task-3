import { buildApp } from "../src/app.js";
import { describe, expect, it } from "vitest";

describe("route contracts", () => {
  it("returns seeded catalog and evaluation summary when DB is prepared", async () => {
    const app = await buildApp();

    const catalogResponse = await app.inject({
      method: "GET",
      url: "/api/catalog"
    });

    expect(catalogResponse.statusCode).toBe(200);
    const catalogBody = catalogResponse.json() as { items: Array<{ id: string }> };
    expect(catalogBody.items.length).toBeGreaterThanOrEqual(12);

    const recommendationResponse = await app.inject({
      method: "POST",
      url: "/api/recommendations",
      payload: {
        query: "배포 전에 manifest 호환성과 changeset 릴리즈 체크를 같이 보고 싶어요",
        desiredCapabilities: ["release-management", "changesets", "semver"],
        preferredCategories: ["ops"],
        environment: {
          locale: "ko-KR",
          clientVersion: "1.2.0",
          transport: "stdio",
          platform: "node"
        },
        maxResults: 3
      }
    });

    expect(recommendationResponse.statusCode).toBe(200);
    const recommendationBody = recommendationResponse.json() as {
      topCandidates: Array<{ catalogId: string }>;
    };
    expect(recommendationBody.topCandidates[0]?.catalogId).toBe("release-check-bot");

    const evalResponse = await app.inject({
      method: "POST",
      url: "/api/evals/run"
    });

    expect(evalResponse.statusCode).toBe(200);
    const evalBody = evalResponse.json() as {
      metrics: { top3Recall: number };
      acceptance: { top3RecallPass: boolean };
    };
    expect(evalBody.metrics.top3Recall).toBeGreaterThanOrEqual(0.9);
    expect(evalBody.acceptance.top3RecallPass).toBe(true);

    await app.close();
  });
});
