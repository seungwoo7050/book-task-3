import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { mockFetchRoutes } from "../testUtils";
import { JobsPage } from "./Jobs";

describe("JobsPage", () => {
  it("creates a job and lets the operator select it", async () => {
    const onSelectJobId = vi.fn();
    const onRefreshJobs = vi.fn(async () => undefined);

    mockFetchRoutes([
      {
        path: "/api/datasets",
        body: { items: [{ id: "dataset-001", name: "sample-transcripts", is_sample: true }] },
      },
      {
        path: "/api/kb-bundles",
        body: { items: [{ id: "bundle-001", name: "sample-kb", is_sample: true }] },
      },
      {
        method: "POST",
        path: "/api/jobs",
        body: {
          job: {
            id: "job-001",
            status: "pending",
            progress_completed: 0,
            progress_total: 2,
            error_summary: "",
            run_id: "run-001",
            run_label: "candidate-run",
            dataset_id: "dataset-001",
            dataset_name: "sample-transcripts",
            kb_bundle_id: "bundle-001",
            kb_bundle_name: "sample-kb",
            evaluation_count: 0,
            avg_score: 0,
            critical_count: 0,
            created_at: "2026-03-08T00:00:00+00:00",
            updated_at: "2026-03-08T00:00:00+00:00",
          },
        },
      },
    ]);

    render(
      <JobsPage jobs={[]} selectedJobId={null} onSelectJobId={onSelectJobId} onRefreshJobs={onRefreshJobs} />,
    );

    expect(await screen.findByText("sample-transcripts (sample)")).toBeDefined();

    fireEvent.change(screen.getByPlaceholderText("candidate-run"), { target: { value: "candidate-run" } });
    fireEvent.click(screen.getByText("job 생성"));

    await waitFor(() => {
      expect(onRefreshJobs).toHaveBeenCalled();
    });
    expect(onSelectJobId).toHaveBeenCalledWith("job-001");
  });
});
