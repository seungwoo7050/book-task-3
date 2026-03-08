import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { MpcDashboard } from "./mcp-dashboard";

type SessionUser = {
  id: string;
  email: string;
  name: string;
  role: "owner" | "operator" | "viewer";
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
};

const fetchMock = vi.fn();
const now = new Date().toISOString();

const ownerSession = {
  user: {
    id: "user-owner-seed",
    email: "owner@study1.local",
    name: "Study1 Owner",
    role: "owner" as const,
    isActive: true,
    createdAt: now,
    updatedAt: now
  },
  settings: {
    id: "default",
    workspaceName: "Study1 OSS Team",
    defaultLocale: "ko-KR",
    defaultClientVersion: "1.2.0",
    evalMinTop3Recall: 0.9,
    compareMinUplift: 0.02,
    updatedAt: now,
    updatedBy: "seed"
  }
};

const viewerSession = {
  ...ownerSession,
  user: {
    id: "user-viewer-seed",
    email: "viewer@study1.local",
    name: "Study1 Viewer",
    role: "viewer" as const,
    isActive: true,
    createdAt: now,
    updatedAt: now
  }
};

function ok(body: unknown) {
  return {
    ok: true,
    json: async () => body
  };
}

function unauthorized() {
  return {
    ok: false,
    status: 401,
    json: async () => ({ message: "Unauthorized" })
  };
}

function createDashboardFetch(initialSession: typeof ownerSession | typeof viewerSession | null) {
  let session = initialSession;
  let jobs = [
    {
      id: "job-seed",
      name: "eval",
      status: "completed",
      createdByUserId: "user-owner-seed",
      createdByEmail: "owner@study1.local",
      payload: {},
      resultSummaryKo: "offline eval이 완료됐고 top3 recall 95.8%를 기록했습니다.",
      errorSummary: null,
      output: { top3Recall: 0.9583 },
      createdAt: now,
      startedAt: now,
      finishedAt: now
    }
  ];

  const catalogEntries = [
    {
      id: "release-check-bot",
      slug: "release-check-bot",
      name: "Release Check Bot",
      version: "1.5.0",
      toolCategory: "ops",
      summaryKo: "릴리즈 점검용 MCP",
      descriptionKo:
        "릴리즈 후보의 changeset, semver, compatibility gate를 함께 검증하는 self-hosted 운영용 MCP입니다.",
      capabilities: ["release-management", "changesets", "semver"],
      koreanUseCases: ["릴리즈 후보 점검", "changeset 검증"],
      differentiationPoints: [
        "changeset 상태와 체크리스트를 같이 보여줍니다.",
        "dry-run 증빙을 남깁니다."
      ],
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
        recommendedFor: ["릴리즈 검토", "changeset 검증"],
        cautionKo: "dry-run only"
      }
    }
  ];

  const users: SessionUser[] = [ownerSession.user, viewerSession.user];

  return vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = new URL(String(input), "http://127.0.0.1:3103");
    const method = init?.method ?? "GET";

    if (url.pathname === "/api/auth/session") {
      return session ? ok(session) : unauthorized();
    }

    if (url.pathname === "/api/auth/login" && method === "POST") {
      session = ownerSession;
      return ok(ownerSession);
    }

    if (url.pathname === "/api/auth/logout" && method === "POST") {
      session = null;
      return ok({ loggedOut: true });
    }

    if (!session) {
      return unauthorized();
    }

    if (url.pathname === "/api/catalog" && method === "GET") {
      return ok({ items: catalogEntries });
    }

    if (url.pathname === "/api/experiments" && method === "GET") {
      return ok({
        items: [
          {
            id: "exp-release-signal",
            name: "release-signal-rerank",
            baselineStrategy: "weighted-baseline-v0",
            candidateStrategy: "signal-rerank-v1",
            trafficSplitPercent: 50,
            status: "running",
            hypothesisKo: "usage signal과 operator feedback이 compare를 안정화한다."
          }
        ]
      });
    }

    if (url.pathname === "/api/release-candidates" && method === "GET") {
      return ok({
        items: [
          {
            id: "rc-release-check-bot-1-5-0",
            name: "release-check-bot v1.5.0",
            manifestId: "release-check-bot",
            previousVersion: "1.4.0",
            releaseVersion: "1.5.0",
            targetClientVersion: "1.2.0",
            releaseNotesKo: "릴리즈 노트",
            requiredDocs: ["docs/install.md"],
            requiredArtifacts: ["docker-compose.yml"],
            deprecatedFieldsUsed: [],
            owner: "release-ops",
            status: "candidate",
            createdAt: now,
            updatedAt: now
          }
        ]
      });
    }

    if (url.pathname === "/api/jobs" && method === "GET") {
      return ok({ items: jobs });
    }

    if (url.pathname === "/api/jobs/job-release-gate" && method === "GET") {
      jobs = [
        {
          id: "job-release-gate",
          name: "release-gate",
          status: "completed",
          createdByUserId: session.user.id,
          createdByEmail: session.user.email,
          payload: { releaseCandidateId: "rc-release-check-bot-1-5-0" },
          resultSummaryKo: "release gate가 PASS로 완료됐습니다.",
          errorSummary: null,
          output: { passed: true, uplift: 0.1146 },
          createdAt: now,
          startedAt: now,
          finishedAt: now
        },
        ...jobs
      ];
      return ok({ item: jobs[0] });
    }

    if (url.pathname === "/api/jobs/release-gate" && method === "POST") {
      return ok({ jobId: "job-release-gate", status: "pending" });
    }

    if (url.pathname === "/api/recommendations/candidate" && method === "POST") {
      return ok({
        requestId: "candidate-1",
        createdAt: now,
        request: {
          query: "릴리즈 질의",
          desiredCapabilities: ["release-management", "changesets", "semver"],
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
            score: 101,
            explanationKo:
              "Release Check Bot는 release-management, changesets, semver 역량이 직접 맞고 self-hosted 운영 절차에 필요한 검증 근거를 제공합니다.",
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
                {
                  type: "capabilityMatch",
                  label: "capability",
                  score: 35,
                  detailKo: "release-management, changesets, semver가 직접 맞습니다."
                }
              ]
            }
          }
        ]
      });
    }

    if (url.pathname === "/api/recommendations" && method === "POST") {
      return ok({
        requestId: "baseline-1",
        createdAt: now,
        request: {
          query: "릴리즈 질의",
          desiredCapabilities: ["release-management", "changesets", "semver"],
          preferredCategories: ["ops"],
          environment: {
            locale: "ko-KR",
            clientVersion: "1.2.0",
            transport: "stdio",
            platform: "node"
          },
          maxResults: 3
        },
        topCandidates: []
      });
    }

    if (url.pathname === "/api/catalog/export" && method === "GET") {
      return ok({
        item: {
          catalogEntries,
          evalCases: [],
          releaseCandidates: []
        }
      });
    }

    if (url.pathname === "/api/usage-events" && method === "GET") {
      return ok({
        items: [],
        totals: { impression: 10, click: 6, accept: 4, dismiss: 1 }
      });
    }

    if (url.pathname === "/api/evals/latest" && method === "GET") {
      return ok({
        latest: {
          id: "eval-1",
          metrics: {
            top3Recall: 0.9583,
            explanationCompleteness: 1,
            forbiddenHitRate: 0
          },
          acceptance: {
            top3RecallPass: true,
            explanationPass: true,
            forbiddenPass: true
          }
        }
      });
    }

    if (url.pathname === "/api/compare/latest" && method === "GET") {
      return ok({
        latest: {
          id: "compare-1",
          metrics: {
            baselineNdcg3: 0.9759,
            candidateNdcg3: 0.9759,
            uplift: 0.1146,
            baselineTop1HitRate: 0.92,
            candidateTop1HitRate: 0.92
          }
        }
      });
    }

    if (url.pathname === "/api/compatibility/latest" && method === "GET") {
      return ok({
        latest: {
          id: "compatibility-1",
          releaseCandidateId: "rc-release-check-bot-1-5-0",
          passed: true,
          checks: []
        }
      });
    }

    if (url.pathname === "/api/release-gate/latest" && method === "GET") {
      return ok({
        latest: {
          id: "gate-1",
          releaseCandidateId: "rc-release-check-bot-1-5-0",
          passed: true,
          reasons: [],
          metrics: {
            top3Recall: 0.9583,
            explanationCompleteness: 1,
            forbiddenHitRate: 0,
            baselineNdcg3: 0.9759,
            candidateNdcg3: 0.9759,
            uplift: 0.1146
          }
        }
      });
    }

    if (url.pathname === "/api/submission/latest" && method === "GET") {
      return ok({
        latest: {
          id: "artifact-1",
          releaseCandidateId: "rc-release-check-bot-1-5-0",
          content: "# Submission Artifact\n\nPASS"
        }
      });
    }

    if (url.pathname === "/api/users" && method === "GET") {
      return ok({ items: users });
    }

    if (url.pathname === "/api/audit-logs" && method === "GET") {
      return ok({
        items: [
          {
            id: "audit-1",
            actorUserId: "user-owner-seed",
            actorEmail: "owner@study1.local",
            action: "auth.login",
            targetType: "session",
            targetId: "session-1",
            detailKo: "사용자가 로그인했습니다.",
            metadata: {},
            createdAt: now
          }
        ]
      });
    }

    if (url.pathname === "/api/settings" && method === "GET") {
      return ok({ item: ownerSession.settings });
    }

    if (url.pathname === "/api/settings" && method === "PUT") {
      return ok({ item: ownerSession.settings });
    }

    if (url.pathname === "/api/usage-events" && method === "POST") {
      return ok({ saved: true });
    }

    if (url.pathname === "/api/users" && method === "POST") {
      return ok({ item: ownerSession.user });
    }

    return ok({});
  });
}

describe("MpcDashboard v3", () => {
  beforeEach(() => {
    fetchMock.mockReset();
    global.fetch = fetchMock;
    vi.stubGlobal("crypto", {
      randomUUID: () => "uuid-1"
    } satisfies Pick<Crypto, "randomUUID">);
  });

  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it("logs in as owner and runs export plus release-gate job flow", async () => {
    fetchMock.mockImplementation(createDashboardFetch(null));

    render(<MpcDashboard />);

    await waitFor(() =>
      expect(screen.getByRole("heading", { name: "MCP OSS 운영 콘솔 로그인" })).toBeInTheDocument()
    );
    fireEvent.click(screen.getByRole("button", { name: "로그인" }));

    await waitFor(() =>
      expect(screen.getByRole("heading", { name: "MCP OSS 운영 콘솔" })).toBeInTheDocument()
    );
    expect(screen.getByRole("heading", { name: "Instance Settings" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Team Access" })).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Candidate 실행" }));
    await waitFor(() =>
      expect(
        screen.getByText(/Release Check Bot는 release-management, changesets, semver 역량이 직접 맞고/i)
      ).toBeInTheDocument()
    );

    fireEvent.click(screen.getByRole("button", { name: "Export Bundle" }));
    await waitFor(() => {
      const textarea = screen.getByPlaceholderText('{"catalogEntries":[...]}') as HTMLTextAreaElement;
      expect(textarea.value).toContain('"catalogEntries"');
    });

    fireEvent.click(screen.getByRole("button", { name: "Release Gate Job" }));
    await waitFor(() =>
      expect(screen.getAllByText("release gate가 PASS로 완료됐습니다.").length).toBeGreaterThan(0)
    );
  });

  it("renders viewer mode as read-only", async () => {
    fetchMock.mockImplementation(createDashboardFetch(viewerSession));

    render(<MpcDashboard />);

    await waitFor(() =>
      expect(screen.getByRole("heading", { name: "MCP OSS 운영 콘솔" })).toBeInTheDocument()
    );
    expect(screen.getByText("viewer는 운영 실행 버튼이 비활성화됩니다.")).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Candidate 실행" })).not.toBeInTheDocument();
    expect(screen.queryByRole("heading", { name: "Team Access" })).not.toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Latest Artifact Preview" })).toBeInTheDocument();
  });
});
