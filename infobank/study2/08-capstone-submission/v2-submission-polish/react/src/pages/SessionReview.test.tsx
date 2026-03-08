import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { SessionReviewPage } from "./SessionReview";
import { mockFetchRoutes } from "../testUtils";

describe("SessionReviewPage", () => {
  it("shows conversation metadata and evaluation traces", async () => {
    mockFetchRoutes([
      {
        path: "/api/conversations",
        body: {
          items: [
            {
              id: "conv-001",
              created_at: "2026-03-07T00:00:00+00:00",
              prompt_version: "v1.0",
              kb_version: "v1.0",
              run_id: "run-001",
              turn_count: 1,
              session_score: 91,
              session_grade: "A",
            },
          ],
        },
      },
      {
        path: "/api/conversations/conv-001",
        body: {
          conversation: {
            id: "conv-001",
            created_at: "2026-03-07T00:00:00+00:00",
            prompt_version: "v1.0",
            kb_version: "v1.0",
            run_id: "run-001",
            turn_count: 1,
            session_score: 91,
            session_grade: "A",
          },
          turns: [
            {
              id: "turn-001",
              turn_index: 1,
              user_message: "해지 위약금이 있나요?",
              assistant_response: "정책상 위약금이 발생할 수 있으니 확인 후 상담원 연결이 필요합니다.",
              retrieved_doc_ids: ["kb-termination", "kb-escalation"],
              evaluation: {
                id: "eval-001",
                grade: "B",
                total_score: 82,
                failure_types: ["ESCALATION_MISS"],
                lineage: {
                  run_label: "v1.1",
                  dataset: "golden-set",
                  trace_id: "trace-123",
                  evaluator_version: "eval-v1",
                  retrieval_version: "retrieval-v1",
                },
                judge_trace: {
                  provider: "openai",
                  model: "gpt-4o-mini",
                  short_circuit: false,
                  short_circuit_reason: null,
                },
              },
            },
          ],
        },
      },
    ]);

    render(<SessionReviewPage />);

    expect(await screen.findByText("세션 리뷰")).toBeDefined();
    expect(await screen.findByText(/run=run-001/)).toBeDefined();
    expect(screen.getByText(/docs: kb-termination, kb-escalation/)).toBeDefined();
    expect(screen.getByText(/trace=trace-123/)).toBeDefined();
    expect(screen.getByText(/openai \/ gpt-4o-mini/)).toBeDefined();
  });
});
