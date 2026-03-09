import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { mockFetchRoutes } from "../testUtils";
import { DatasetsPage } from "./Datasets";

describe("DatasetsPage", () => {
  it("loads datasets and submits JSONL uploads", async () => {
    const fetchMock = mockFetchRoutes([
      {
        path: "/api/datasets",
        body: {
          items: [{ id: "sample-ds", name: "sample-transcripts", source_filename: "sample.jsonl", record_count: 4, is_sample: true, created_at: "2026-03-08T00:00:00+00:00" }],
        },
      },
      {
        method: "POST",
        path: "/api/datasets/import",
        body: { dataset_id: "dataset-001", record_count: 2, warnings: [] },
      },
      {
        path: "/api/datasets",
        body: {
          items: [
            { id: "dataset-001", name: "support-transcripts", source_filename: "support.jsonl", record_count: 2, is_sample: false, created_at: "2026-03-08T00:00:00+00:00" },
          ],
        },
      },
    ]);

    render(<DatasetsPage />);

    expect(await screen.findByText("sample-transcripts")).toBeDefined();

    const input = screen.getByLabelText("Transcript JSONL") as HTMLInputElement;
    const file = new File(['{"conversation_external_id":"c1","turn_index":1,"user_message":"u","assistant_response":"a"}'], "support.jsonl", {
      type: "application/x-ndjson",
    });
    fireEvent.change(input, { target: { files: [file] } });
    fireEvent.change(screen.getByPlaceholderText("support-transcripts"), { target: { value: "support-transcripts" } });
    fireEvent.click(screen.getByText("dataset 업로드"));

    expect(await screen.findByText("support-transcripts")).toBeDefined();
    expect(fetchMock).toHaveBeenCalled();
  });
});
