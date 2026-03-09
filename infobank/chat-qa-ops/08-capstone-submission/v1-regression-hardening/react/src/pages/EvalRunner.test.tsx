import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { EvalRunnerPage } from "./EvalRunner";
import { mockFetchRoutes } from "../testUtils";

describe("EvalRunnerPage", () => {
  it("submits golden-set runs with run metadata and renders the summary", async () => {
    const fetchMock = mockFetchRoutes([
      {
        method: "POST",
        path: "/api/golden-set/run",
        body: {
          run_id: "run-101",
          run_label: "v1.1",
          dataset: "golden-set",
          count: 30,
          avg_score: 88.1,
          critical_count: 1,
          pass_count: 21,
          fail_count: 9,
        },
      },
    ]);

    render(<EvalRunnerPage />);

    fireEvent.click(screen.getByText("골든셋 평가 실행"));

    expect(await screen.findByText("run_id: run-101")).toBeDefined();
    expect(screen.getByText("assertion pass/fail: 21 / 9")).toBeDefined();
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(fetchMock.mock.calls[0]?.[1]?.body).toContain("\"run_label\":\"v1.1\"");
    expect(fetchMock.mock.calls[0]?.[1]?.body).toContain("\"baseline_label\":\"v1.0\"");
  });
});
