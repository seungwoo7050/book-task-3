import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { mockFetchRoutes } from "../testUtils";
import { SessionReviewPage } from "./SessionReview";

describe("SessionReviewPage", () => {
  it("shows run-scoped conversation detail and traces", async () => {
    mockFetchRoutes([
      {
        path: "/api/conversations?job_id=job-001",
        body: {
          items: [
            {
              id: "conv-001",
              external_id: "sample-conv-001",
              created_at: "2026-03-07T00:00:00+00:00",
              prompt_version: "imported-transcript",
              kb_version: "uploaded-kb",
              run_id: "run-001",
              turn_count: 1,
              session_score: 91,
              session_grade: "A",
            },
          ],
        },
      },
      {
        path: "/api/conversations/conv-001?job_id=job-001",
        body: {
          conversation: {
            id: "conv-001",
            external_id: "sample-conv-001",
            created_at: "2026-03-07T00:00:00+00:00",
            prompt_version: "imported-transcript",
            kb_version: "uploaded-kb",
            run_id: "run-001",
            session_score: 91,
            session_grade: "A",
          },
          turns: [
            {
              id: "turn-001",
              turn_index: 1,
              user_message: "환불이 거절됐어요.",
              assistant_response: "전문 부서 이관 기준을 확인해야 합니다.",
              retrieved_doc_ids: ["bundle::policies__refund.md"],
              evaluation: {
                id: "eval-001",
                grade: "B",
                total_score: 82,
                failure_types: ["ESCALATION_MISS"],
                lineage: {
                  run_label: "candidate-run",
                  dataset: "shared-dataset",
                  trace_id: "trace-123",
                  run_id: "run-001",
                  retrieval_version: "retrieval-v2",
                },
                judge_trace: {
                  provider: "heuristic",
                  model: "rule-based",
                  short_circuit: false,
                  short_circuit_reason: null,
                },
              },
            },
          ],
        },
      },
    ]);

    render(<SessionReviewPage selectedJobId="job-001" />);

    expect(await screen.findByText("Session Review")).toBeDefined();
    expect(await screen.findByText(/external=sample-conv-001/)).toBeDefined();
    expect(screen.getByText(/bundle::policies__refund.md/)).toBeDefined();
    expect(screen.getByText(/trace=trace-123/)).toBeDefined();
    expect(screen.getByText(/heuristic \/ rule-based/)).toBeDefined();
  });
});
