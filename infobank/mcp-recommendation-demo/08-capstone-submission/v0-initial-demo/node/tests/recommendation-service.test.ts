import { catalogSeeds } from "@study1-v0/shared";
import { describe, expect, it } from "vitest";
import { buildExplanationKo, recommendCatalog, scoreCatalogEntry } from "../src/services/recommendation-service.js";

describe("recommendation service", () => {
  it("prioritizes release MCPs for release queries", () => {
    const releaseBot = catalogSeeds.find((item) => item.id === "release-check-bot");
    const docsSearch = catalogSeeds.find((item) => item.id === "korean-docs-search");

    expect(releaseBot).toBeDefined();
    expect(docsSearch).toBeDefined();

    const request = {
      query: "릴리즈 전에 changeset과 체크리스트를 같이 확인하고 싶어요",
      desiredCapabilities: ["release-management", "changesets", "changelog"],
      preferredCategories: ["ops" as const],
      environment: {
        locale: "ko-KR",
        clientVersion: "1.2.0",
        transport: "stdio" as const,
        platform: "node" as const
      },
      maxResults: 3
    };

    const releaseScore = scoreCatalogEntry(request, releaseBot!);
    const docsScore = scoreCatalogEntry(request, docsSearch!);

    expect(releaseScore.totalScore).toBeGreaterThan(docsScore.totalScore);

    const result = recommendCatalog(request, catalogSeeds);
    expect(result.topCandidates[0]?.catalogId).toBe("release-check-bot");
  });

  it("keeps explanation within capability, differentiation, compatibility axes", () => {
    const entry = catalogSeeds.find((item) => item.id === "release-check-bot")!;
    const request = {
      query: "릴리즈 검증을 해주세요",
      desiredCapabilities: ["release-management", "changesets"],
      preferredCategories: ["ops" as const],
      environment: {
        locale: "ko-KR",
        clientVersion: "1.2.0",
        transport: "stdio" as const,
        platform: "node" as const
      },
      maxResults: 3
    };

    const result = recommendCatalog(request, [entry]);
    const explanation = buildExplanationKo(entry, request, result.topCandidates[0]!.trace);

    expect(explanation).toContain("changeset");
    expect(explanation).toContain(entry.differentiationPoints[0]);
    expect(explanation).toContain("현재 클라이언트 1.2.0");
    expect(explanation).not.toContain("보장");
    expect(explanation).not.toContain("무조건");
  });
});
