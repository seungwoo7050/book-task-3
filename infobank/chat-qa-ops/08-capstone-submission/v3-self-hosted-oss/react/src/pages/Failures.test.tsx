import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { mockFetchRoutes } from "../testUtils";
import { FailuresPage } from "./Failures";

describe("FailuresPage", () => {
  it("renders failure aggregates for the selected job", async () => {
    mockFetchRoutes([
      {
        path: "/api/dashboard/failures?job_id=job-001",
        body: {
          items: [
            { failure_type: "FORBIDDEN_PROMISE", count: 1, critical_count: 0, avg_score: 72.5 },
            { failure_type: "ESCALATION_MISS", count: 1, critical_count: 0, avg_score: 68.1 },
          ],
        },
      },
    ]);

    render(<FailuresPage selectedJobId="job-001" />);

    expect(await screen.findByText("Failures")).toBeDefined();
    expect(screen.getByText("유형 수: 2")).toBeDefined();
    expect(screen.getByText(/selected job: job-001/)).toBeDefined();
    expect(screen.getByText("금지된 약속 (FORBIDDEN_PROMISE)")).toBeDefined();
  });
});
