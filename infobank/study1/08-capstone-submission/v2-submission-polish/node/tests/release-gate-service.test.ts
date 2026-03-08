import { describe, expect, it } from "vitest";
import { runReleaseGate } from "../src/services/release-gate-service.js";

const candidateBase = {
  id: "rc-gate",
  name: "release-check-bot v1.5.0",
  manifestId: "release-check-bot",
  previousVersion: "1.4.0",
  releaseVersion: "1.5.0",
  targetClientVersion: "1.2.0",
  releaseNotesKo:
    "변경 요약: dry-run 릴리즈 흐름을 정리했습니다.\n검증: eval, compare, compatibility, gate를 모두 다시 돌렸습니다.\n리스크: tested version 밖 클라이언트는 추가 검증이 필요합니다.",
  requiredDocs: ["package.json"],
  requiredArtifacts: ["node/package.json"],
  deprecatedFieldsUsed: [],
  owner: "release-ops",
  status: "candidate" as const,
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString()
};

describe("runReleaseGate", () => {
  it("passes when compatibility, eval, compare, and docs all satisfy the threshold", () => {
    const report = runReleaseGate(
      candidateBase,
      {
        id: "compat-1",
        releaseCandidateId: candidateBase.id,
        candidateVersion: candidateBase.releaseVersion,
        passed: true,
        checks: [],
        issues: [],
        checkedAt: new Date().toISOString()
      },
      {
        metrics: { top3Recall: 1, explanationCompleteness: 1, forbiddenHitRate: 0 },
        acceptance: { top3RecallPass: true, explanationPass: true, forbiddenPass: true }
      },
      {
        metrics: {
          baselineNdcg3: 0.9,
          candidateNdcg3: 0.94,
          uplift: 0.04,
          baselineTop1HitRate: 0.8,
          candidateTop1HitRate: 0.9
        }
      }
    );

    expect(report.passed).toBe(true);
    expect(report.reasons).toEqual([]);
  });

  it("fails when docs are missing or uplift is below the gate threshold", () => {
    const report = runReleaseGate(
      {
        ...candidateBase,
        requiredDocs: ["docs/does-not-exist.md"]
      },
      {
        id: "compat-2",
        releaseCandidateId: candidateBase.id,
        candidateVersion: candidateBase.releaseVersion,
        passed: true,
        checks: [],
        issues: [],
        checkedAt: new Date().toISOString()
      },
      {
        metrics: { top3Recall: 1, explanationCompleteness: 1, forbiddenHitRate: 0 },
        acceptance: { top3RecallPass: true, explanationPass: true, forbiddenPass: true }
      },
      {
        metrics: {
          baselineNdcg3: 0.92,
          candidateNdcg3: 0.92,
          uplift: 0,
          baselineTop1HitRate: 0.82,
          candidateTop1HitRate: 0.82
        }
      }
    );

    expect(report.passed).toBe(false);
    expect(report.reasons.join(" ")).toMatch(/누락|uplift/);
  });
});
