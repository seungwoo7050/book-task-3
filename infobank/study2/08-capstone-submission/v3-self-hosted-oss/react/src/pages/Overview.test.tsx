import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { mockFetchRoutes } from "../testUtils";
import { OverviewPage } from "./Overview";

describe("OverviewPage", () => {
  it("renders scoped overview metrics and version compare data", async () => {
    mockFetchRoutes([
      {
        path: "/api/dashboard/overview?job_id=job-001",
        body: {
          avg_score: 87.5,
          fail_rate: 0,
          critical_count: 0,
          evaluation_count: 2,
          avg_latency_ms: 0,
          grade_distribution: { A: 1, B: 1 },
          failure_top: [{ failure_type: "FORBIDDEN_PROMISE", count: 1 }],
          run_labels: ["baseline-run", "candidate-run"],
          selected_run_id: "run-001",
          selected_job_id: "job-001",
        },
      },
      {
        path: "/api/dashboard/version-compare?baseline=baseline-run&candidate=candidate-run&dataset=shared-dataset",
        body: {
          result: {
            baseline: "baseline-run",
            candidate: "candidate-run",
            dataset: "shared-dataset",
            baseline_avg: 82.4,
            candidate_avg: 87.5,
            baseline_critical: 1,
            candidate_critical: 0,
            baseline_pass_count: 1,
            candidate_pass_count: 2,
            baseline_fail_count: 1,
            candidate_fail_count: 0,
            baseline_failures: { MISSING_REQUIRED_EVIDENCE_DOC: 1 },
            candidate_failures: {},
            delta: 5.1,
            pass_delta: 1,
            fail_delta: -1,
            critical_delta: -1,
          },
        },
      },
    ]);

    render(<OverviewPage selectedJobId="job-001" />);

    expect(await screen.findByText("Overview")).toBeDefined();
    expect(screen.getByText("87.5")).toBeDefined();
    expect(screen.getByText(/selected run=run-001/)).toBeDefined();

    fireEvent.click(screen.getByText("비교 로드"));

    expect(await screen.findByText(/score=5.1/)).toBeDefined();
    expect(screen.getByText(/candidate-run/)).toBeDefined();
  });
});
