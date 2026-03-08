import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { OverviewPage } from "./Overview";
import { mockFetchRoutes } from "../testUtils";

describe("OverviewPage", () => {
  it("renders overview metrics and loads version compare data", async () => {
    mockFetchRoutes([
      {
        path: "/api/dashboard/overview",
        body: {
          avg_score: 84.06,
          fail_rate: 6.67,
          critical_count: 2,
          evaluation_count: 30,
          avg_latency_ms: 104.2,
          grade_distribution: { A: 12, B: 10, C: 4, D: 2, F: 2 },
          failure_top: [{ failure_type: "FORBIDDEN_PROMISE", count: 4 }],
          run_labels: ["v1.0", "v1.1"],
        },
      },
      {
        path: "/api/dashboard/version-compare?baseline=v1.0&candidate=v1.1&dataset=golden-set",
        body: {
          result: {
            baseline: "v1.0",
            candidate: "v1.1",
            dataset: "golden-set",
            baseline_avg: 84.06,
            candidate_avg: 88.1,
            baseline_critical: 2,
            candidate_critical: 1,
            baseline_pass_count: 16,
            candidate_pass_count: 21,
            baseline_fail_count: 14,
            candidate_fail_count: 9,
            baseline_failures: { MISSING_REQUIRED_EVIDENCE_DOC: 8 },
            candidate_failures: { MISSING_REQUIRED_EVIDENCE_DOC: 3 },
            delta: 4.04,
            pass_delta: 5,
            fail_delta: -5,
            critical_delta: -1,
          },
        },
      },
    ]);

    render(<OverviewPage />);

    expect(await screen.findByText("개요")).toBeDefined();
    expect(screen.getByText("84.06")).toBeDefined();
    expect(screen.getByText("v1.1")).toBeDefined();

    fireEvent.click(screen.getByText("비교 로드"));

    expect(await screen.findByText("점수 변화")).toBeDefined();
    expect(screen.getByText("4.04")).toBeDefined();
    expect(screen.getAllByText(/근거 문서 필수 근거 누락|MISSING_REQUIRED_EVIDENCE_DOC/).length).toBeGreaterThan(0);
  });
});
