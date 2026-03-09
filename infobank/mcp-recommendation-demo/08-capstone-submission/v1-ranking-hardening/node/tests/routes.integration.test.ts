import { buildApp } from "../src/app.js";
import { describe, expect, it } from "vitest";

describe("route contracts", () => {
  it("returns seeded catalog, compare results, and reranked recommendations when DB is prepared", async () => {
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

    const candidateResponse = await app.inject({
      method: "POST",
      url: "/api/recommendations/candidate",
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

    expect(candidateResponse.statusCode).toBe(200);

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

    const compareResponse = await app.inject({
      method: "POST",
      url: "/api/compare/run",
      payload: {
        experimentId: "exp-release-signal"
      }
    });

    expect(compareResponse.statusCode).toBe(200);
    const compareBody = compareResponse.json() as {
      metrics: { candidateNdcg3: number; baselineNdcg3: number };
    };
    expect(compareBody.metrics.candidateNdcg3).toBeGreaterThanOrEqual(
      compareBody.metrics.baselineNdcg3
    );

    await app.close();
  });
});
