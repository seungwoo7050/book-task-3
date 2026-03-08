import { catalogSeeds } from "@study1-v3/shared";
import { describe, expect, it } from "vitest";
import { runCompatibilityGate } from "../src/services/compatibility-service.js";

const releaseCheckBot = catalogSeeds.find((item) => item.id === "release-check-bot")!;

describe("runCompatibilityGate", () => {
  it("passes for the seeded release candidate shape", () => {
    const report = runCompatibilityGate(
      {
        id: "rc-pass",
        name: "release-check-bot v1.5.0",
        manifestId: "release-check-bot",
        previousVersion: "1.4.0",
        releaseVersion: "1.5.0",
        targetClientVersion: "1.2.0",
        releaseNotesKo:
          "변경 요약: 릴리즈 dry-run 흐름을 정리했습니다.\n검증: eval과 compare를 재실행했습니다.\n리스크: tested client version 밖은 추가 확인이 필요합니다.",
        requiredDocs: ["package.json"],
        requiredArtifacts: ["node/package.json"],
        deprecatedFieldsUsed: [],
        owner: "release-ops",
        status: "candidate",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      },
      releaseCheckBot
    );

    expect(report.passed).toBe(true);
    expect(report.issues).toEqual([]);
  });

  it("fails when deprecated fields or semver metadata are inconsistent", () => {
    const report = runCompatibilityGate(
      {
        id: "rc-fail",
        name: "release-check-bot v2.0.0",
        manifestId: "release-check-bot",
        previousVersion: "1.5.0",
        releaseVersion: "2.0.0",
        targetClientVersion: "1.2.0",
        releaseNotesKo:
          "변경 요약: major bump입니다.\n검증: 없음.\n리스크: breaking changes 정리가 빠졌습니다.",
        requiredDocs: ["package.json"],
        requiredArtifacts: ["node/package.json"],
        deprecatedFieldsUsed: ["legacyPrompt"],
        owner: "release-ops",
        status: "candidate",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      },
      releaseCheckBot
    );

    expect(report.passed).toBe(false);
    expect(report.issues.join(" ")).toMatch(/deprecated field|breaking change/);
  });
});
