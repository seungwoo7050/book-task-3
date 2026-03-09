import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { MpcDashboard } from "./mcp-dashboard";

const fetchMock = vi.fn();

describe("MpcDashboard", () => {
  beforeEach(() => {
    fetchMock.mockReset();
    global.fetch = fetchMock;
  });

  it("renders catalog and executes recommendation flow", async () => {
    fetchMock
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          items: [
            {
              id: "release-check-bot",
              slug: "release-check-bot",
              name: "Release Check Bot",
              version: "1.5.0",
              toolCategory: "ops",
              summaryKo: "릴리즈를 점검합니다.",
              descriptionKo: "릴리즈 흐름을 점검합니다.",
              capabilities: ["release-management", "changesets", "changelog"],
              koreanUseCases: ["릴리즈 후보 점검", "changeset 검증"],
              differentiationPoints: ["changeset 상태와 체크리스트를 같이 보여줍니다.", "dry-run 증빙을 남깁니다."],
              supportedLocales: ["ko-KR"],
              runtime: {
                protocolVersion: "1.0",
                nodeRange: ">=20 <26",
                transports: ["stdio"],
                platforms: ["node"]
              },
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
                recommendedFor: ["릴리즈 검토", "changeset 점검"],
                cautionKo: "dry-run only"
              }
            }
          ]
        })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ latest: null })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          requestId: "req-1",
          createdAt: new Date().toISOString(),
          request: {
            query: "릴리즈 질의",
            desiredCapabilities: ["release-management"],
            preferredCategories: ["ops"],
            environment: {
              locale: "ko-KR",
              clientVersion: "1.2.0",
              transport: "stdio",
              platform: "node"
            },
            maxResults: 3
          },
          topCandidates: [
            {
              catalogId: "release-check-bot",
              rank: 1,
              score: 91,
              explanationKo: "Release Check Bot는 release-management 역량이 직접 맞습니다.",
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
                  { type: "capabilityMatch", label: "capability", score: 35, detailKo: "release-management 역량이 직접 맞습니다." },
                  { type: "differentiation", label: "differentiation", score: 8, detailKo: "changeset 상태와 체크리스트를 같이 보여줍니다." },
                  { type: "compatibility", label: "compatibility", score: 15, detailKo: "현재 클라이언트 1.2.0 / stdio / node 환경과 호환됩니다." }
                ]
              }
            }
          ]
        })
      });

    render(<MpcDashboard />);

    await waitFor(() => expect(screen.getByText("MCP 추천 운영 데모")).toBeInTheDocument());
    fireEvent.click(screen.getByRole("button", { name: "추천 실행" }));

    await waitFor(() => expect(screen.getByText(/release-check-bot/i)).toBeInTheDocument());
  });
});
