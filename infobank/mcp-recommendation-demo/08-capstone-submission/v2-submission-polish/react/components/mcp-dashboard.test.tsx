import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { MpcDashboard } from "./mcp-dashboard";

const fetchMock = vi.fn();

describe("MpcDashboard v2", () => {
  beforeEach(() => {
    fetchMock.mockReset();
    global.fetch = fetchMock;
    vi.stubGlobal("crypto", {
      randomUUID: () => "uuid-1"
    } satisfies Pick<Crypto, "randomUUID">);

    fetchMock.mockImplementation(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);

      if (url.endsWith("/api/catalog")) {
        return {
          ok: true,
          json: async () => ({
            items: [
              {
                id: "release-check-bot",
                slug: "release-check-bot",
                name: "Release Check Bot",
                version: "1.5.0",
                toolCategory: "ops",
                summaryKo: "릴리즈 점검용 MCP",
                descriptionKo: "릴리즈 점검용 MCP 설명입니다. submission polish 단계에서도 충분한 길이를 유지합니다.",
                capabilities: ["release-management", "changesets", "semver"],
                koreanUseCases: ["릴리즈 후보 점검", "changeset 검증"],
                differentiationPoints: ["changeset 상태와 체크리스트를 같이 보여줍니다.", "dry-run 증빙을 남깁니다."],
                supportedLocales: ["ko-KR"],
                runtime: { protocolVersion: "1.0", nodeRange: ">=20 <26", transports: ["stdio"], platforms: ["node"] },
                maturity: { stage: "production", score: 94 },
                compatibility: {
                  minimumClientVersion: "1.0.0",
                  maximumClientVersion: "2.0.0",
                  testedClientVersions: ["1.2.0"],
                  deprecatedClientVersions: [],
                  breakingChanges: []
                },
                operational: {
                  maintainer: "Release Engineering",
                  slaTier: "mission-critical",
                  securityReview: true,
                  releaseChannel: "stable"
                },
                tags: ["릴리즈", "changesets"],
                freshnessScore: 0.95,
                exposure: {
                  userFacingSummaryKo: "릴리즈를 검증합니다.",
                  recommendedFor: ["릴리즈 검토", "changeset 검증"],
                  cautionKo: "dry-run only"
                }
              }
            ]
          })
        };
      }

      if (url.endsWith("/api/evals/latest")) {
        return { ok: true, json: async () => ({ latest: null }) };
      }

      if (url.endsWith("/api/compare/latest")) {
        return { ok: true, json: async () => ({ latest: null }) };
      }

      if (url.endsWith("/api/experiments")) {
        if (init?.method === "POST") {
          return { ok: true, json: async () => ({ saved: true }) };
        }
        return {
          ok: true,
          json: async () => ({
            items: [
              {
                id: "exp-release-signal",
                name: "release-signal-rerank",
                baselineStrategy: "weighted-baseline-v0",
                candidateStrategy: "signal-rerank-v1",
                trafficSplitPercent: 50,
                status: "running",
                hypothesisKo: "usage signal을 넣으면 정렬이 개선된다."
              }
            ]
          })
        };
      }

      if (url.endsWith("/api/usage-events")) {
        if (init?.method === "POST") {
          return { ok: true, json: async () => ({ saved: true }) };
        }
        return {
          ok: true,
          json: async () => ({
            items: [],
            totals: { impression: 10, click: 6, accept: 4, dismiss: 1 }
          })
        };
      }

      if (url.endsWith("/api/release-candidates")) {
        return {
          ok: true,
          json: async () => ({
            items: [
              {
                id: "rc-release-check-bot-1-5-0",
                name: "release-check-bot v1.5.0",
                manifestId: "release-check-bot",
                previousVersion: "1.4.0",
                releaseVersion: "1.5.0",
                targetClientVersion: "1.2.0",
                releaseNotesKo:
                  "변경 요약: dry-run 릴리즈 흐름을 정리했습니다.\n검증: eval, compare, compatibility, gate를 다시 실행했습니다.\n리스크: tested version 밖 클라이언트는 추가 검증이 필요합니다.",
                requiredDocs: ["docs/README.md"],
                requiredArtifacts: [".changeset/config.json"],
                deprecatedFieldsUsed: [],
                owner: "release-ops",
                status: "candidate",
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString()
              }
            ]
          })
        };
      }

      if (url.endsWith("/api/compatibility/latest")) {
        return { ok: true, json: async () => ({ latest: null }) };
      }

      if (url.endsWith("/api/release-gate/latest")) {
        return { ok: true, json: async () => ({ latest: null }) };
      }

      if (url.endsWith("/api/submission/latest")) {
        return { ok: true, json: async () => ({ latest: null }) };
      }

      if (url.endsWith("/api/recommendations/candidate")) {
        return {
          ok: true,
          json: async () => ({
            requestId: "candidate-1",
            createdAt: new Date().toISOString(),
            request: {
              query: "릴리즈 질의",
              desiredCapabilities: ["release-management"],
              preferredCategories: ["ops"],
              environment: { locale: "ko-KR", clientVersion: "1.2.0", transport: "stdio", platform: "node" },
              maxResults: 3
            },
            topCandidates: [
              {
                catalogId: "release-check-bot",
                rank: 1,
                score: 101,
                explanationKo: "candidate 정렬에서 release-check-bot가 강화되었습니다.",
                trace: {
                  candidateId: "release-check-bot",
                  totalScore: 101,
                  breakdown: {
                    intent: 20,
                    capability: 35,
                    category: 10,
                    locale: 10,
                    compatibility: 15,
                    maturity: 9.4,
                    freshness: 4.6
                  },
                  reasons: [
                    { type: "capabilityMatch", label: "capability", score: 35, detailKo: "release-management가 맞습니다." },
                    { type: "differentiation", label: "differentiation", score: 8, detailKo: "changeset 상태와 체크리스트를 같이 보여줍니다." },
                    { type: "compatibility", label: "compatibility", score: 15, detailKo: "현재 클라이언트 1.2.0 / stdio / node 환경과 호환됩니다." }
                  ]
                }
              }
            ]
          })
        };
      }

      if (url.endsWith("/api/recommendations")) {
        return {
          ok: true,
          json: async () => ({
            requestId: "baseline-1",
            createdAt: new Date().toISOString(),
            request: {
              query: "릴리즈 질의",
              desiredCapabilities: ["release-management"],
              preferredCategories: ["ops"],
              environment: { locale: "ko-KR", clientVersion: "1.2.0", transport: "stdio", platform: "node" },
              maxResults: 3
            },
            topCandidates: [
              {
                catalogId: "release-check-bot",
                rank: 1,
                score: 91,
                explanationKo: "baseline 정렬의 release-check-bot",
                trace: {
                  candidateId: "release-check-bot",
                  totalScore: 91,
                  breakdown: {
                    intent: 20,
                    capability: 35,
                    category: 10,
                    locale: 10,
                    compatibility: 15,
                    maturity: 9.4,
                    freshness: 4.6
                  },
                  reasons: [
                    { type: "capabilityMatch", label: "capability", score: 35, detailKo: "release-management가 맞습니다." },
                    { type: "differentiation", label: "differentiation", score: 8, detailKo: "changeset 상태와 체크리스트를 같이 보여줍니다." },
                    { type: "compatibility", label: "compatibility", score: 15, detailKo: "현재 클라이언트 1.2.0 / stdio / node 환경과 호환됩니다." }
                  ]
                }
              }
            ]
          })
        };
      }

      if (url.endsWith("/api/evals/run")) {
        return {
          ok: true,
          json: async () => ({
            id: "eval-1",
            metrics: { top3Recall: 1, explanationCompleteness: 1, forbiddenHitRate: 0 }
          })
        };
      }

      if (url.endsWith("/api/compare/run")) {
        return {
          ok: true,
          json: async () => ({
            id: "compare-1",
            metrics: {
              baselineNdcg3: 0.84,
              candidateNdcg3: 0.91,
              uplift: 0.07,
              baselineTop1HitRate: 0.75,
              candidateTop1HitRate: 0.92
            }
          })
        };
      }

      if (url.endsWith("/api/compatibility/run")) {
        return {
          ok: true,
          json: async () => ({
            id: "compat-1",
            releaseCandidateId: "rc-release-check-bot-1-5-0",
            candidateVersion: "1.5.0",
            passed: true,
            checks: [],
            issues: [],
            checkedAt: new Date().toISOString()
          })
        };
      }

      if (url.endsWith("/api/release-gate/run")) {
        return {
          ok: true,
          json: async () => ({
            id: "gate-1",
            releaseCandidateId: "rc-release-check-bot-1-5-0",
            passed: true,
            reasons: [],
            metrics: {
              top3Recall: 1,
              explanationCompleteness: 1,
              forbiddenHitRate: 0,
              baselineNdcg3: 0.84,
              candidateNdcg3: 0.91,
              uplift: 0.07
            },
            checkedAt: new Date().toISOString()
          })
        };
      }

      if (url.endsWith("/api/submission/export")) {
        return {
          ok: true,
          json: async () => ({
            id: "artifact-1",
            releaseCandidateId: "rc-release-check-bot-1-5-0",
            format: "markdown",
            content: "# release-check-bot v1.5.0\n\n## Release Notes\n변경 요약: dry-run 릴리즈 흐름을 정리했습니다.",
            createdAt: new Date().toISOString()
          })
        };
      }

      if (
        url.includes("/api/catalog/") ||
        url.includes("/api/experiments/") ||
        url.includes("/api/release-candidates/")
      ) {
        return { ok: true, json: async () => ({ saved: true, deleted: true }) };
      }

      if (url.endsWith("/api/feedback")) {
        return { ok: true, json: async () => ({ saved: true }) };
      }

      throw new Error(`Unhandled fetch for ${url}`);
    });
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("renders candidate recommendation and release gate artifact workflow", async () => {
    render(<MpcDashboard />);

    await waitFor(() => expect(screen.getByText("MCP 제출 운영 콘솔")).toBeInTheDocument());
    fireEvent.click(screen.getByRole("button", { name: "Candidate 실행" }));

    await waitFor(() =>
      expect(screen.getByText(/candidate 정렬에서 release-check-bot/i)).toBeInTheDocument()
    );

    fireEvent.click(screen.getByRole("button", { name: "Release Gate 실행" }));

    await waitFor(() => expect(screen.getAllByText("PASS")).toHaveLength(2));
    await waitFor(() => expect(screen.getByText(/## Release Notes/i)).toBeInTheDocument());
  });
});
