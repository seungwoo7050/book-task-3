import { catalogSeeds } from "@study1-v3/shared";
import { describe, expect, it } from "vitest";
import { recommendCatalog } from "../src/services/recommendation-service.js";
import { rerankCatalog } from "../src/services/rerank-service.js";

describe("rerank service", () => {
  it("boosts candidates with stronger usage and feedback signals", () => {
    const request = {
      query: "릴리즈 전에 changeset과 semver를 같이 검토하고 싶어요",
      desiredCapabilities: ["release-management", "changesets", "semver"],
      preferredCategories: ["ops" as const],
      environment: {
        locale: "ko-KR",
        clientVersion: "1.2.0",
        transport: "stdio" as const,
        platform: "node" as const
      },
      maxResults: 3
    };

    const baseline = recommendCatalog(request, catalogSeeds);
    const reranked = rerankCatalog(
      request,
      catalogSeeds,
      [
        {
          id: "u1",
          recommendationRunId: "seed",
          catalogId: "release-check-bot",
          action: "impression",
          actor: "user",
          createdAt: new Date().toISOString(),
          metadata: {}
        },
        {
          id: "u2",
          recommendationRunId: "seed",
          catalogId: "release-check-bot",
          action: "click",
          actor: "user",
          createdAt: new Date().toISOString(),
          metadata: {}
        },
        {
          id: "u3",
          recommendationRunId: "seed",
          catalogId: "release-check-bot",
          action: "accept",
          actor: "user",
          createdAt: new Date().toISOString(),
          metadata: {}
        }
      ],
      [
        {
          id: "f1",
          recommendationRunId: "seed",
          catalogId: "release-check-bot",
          scoreDelta: 2,
          noteKo: "릴리즈 시나리오 적합",
          reviewer: "ops",
          createdAt: new Date().toISOString()
        }
      ]
    );

    expect(reranked.topCandidates[0]?.catalogId).toBe("release-check-bot");
    expect(reranked.topCandidates[0]!.score).toBeGreaterThanOrEqual(
      baseline.topCandidates[0]!.score
    );
  });
});
