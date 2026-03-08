import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { FailuresPage } from "./Failures";
import { mockFetchRoutes } from "../testUtils";

describe("FailuresPage", () => {
  it("renders failure aggregates from the dashboard API", async () => {
    mockFetchRoutes([
      {
        path: "/api/dashboard/failures",
        body: {
          items: [
            { failure_type: "FORBIDDEN_PROMISE", count: 4, critical_count: 1, avg_score: 45.5 },
            { failure_type: "ESCALATION_MISS", count: 2, critical_count: 0, avg_score: 68.4 },
          ],
        },
      },
    ]);

    render(<FailuresPage />);

    expect(await screen.findByText("실패 분석")).toBeDefined();
    expect(screen.getByText("유형 수: 2")).toBeDefined();
    expect(screen.getByText("금지된 약속 (FORBIDDEN_PROMISE)")).toBeDefined();
    expect(screen.getByText("상담원 이관 누락 (ESCALATION_MISS)")).toBeDefined();
  });
});
