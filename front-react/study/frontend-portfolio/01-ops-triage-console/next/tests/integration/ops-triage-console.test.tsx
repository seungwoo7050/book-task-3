import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { useState } from "react";
import { describe, expect, it, vi } from "vitest";
import { QueryProvider } from "@/components/providers/query-client-provider";
import { defaultIssueQuery } from "@/lib/constants";
import { configureDemoRuntime } from "@/lib/service-admin";
import {
  useBulkIssueMutation,
  useDashboardSummary,
  useIssueDetail,
  useIssueList,
  useIssueMutation,
  type ConsoleToast,
} from "@/hooks/use-ops-triage";

function IntegrationHarness() {
  const [query, setQuery] = useState(defaultIssueQuery);
  const [toast, setToast] = useState<ConsoleToast | null>(null);

  const issueListQuery = useIssueList(query);
  const detailQuery = useIssueDetail("OPS-101");
  const summaryQuery = useDashboardSummary();
  const issueMutation = useIssueMutation(setToast);
  const bulkMutation = useBulkIssueMutation("OPS-101", setToast);

  return (
    <div>
      <p data-testid="visible-ids">
        {issueListQuery.data?.items.map((issue) => issue.id).join(",") ?? "loading"}
      </p>
      <p data-testid="status-map">
        {issueListQuery.data?.items
          .map((issue) => `${issue.id}:${issue.status}`)
          .join("|") ?? "loading"}
      </p>
      <p data-testid="detail-status">{detailQuery.data?.status ?? "loading"}</p>
      <p data-testid="untriaged-count">
        {summaryQuery.data?.untriagedCount ?? "loading"}
      </p>
      <button
        type="button"
        onClick={() =>
          setQuery({
            ...defaultIssueQuery,
            status: ["investigating"],
          })
        }
      >
        Filter investigating
      </button>
      <button
        type="button"
        onClick={() =>
          issueMutation.updateOne({
            issueId: "OPS-101",
            patch: { status: "resolved" },
          })
        }
      >
        Resolve OPS-101
      </button>
      <button
        type="button"
        onClick={() =>
          bulkMutation.applyBulk({
            issueIds: ["OPS-102", "OPS-106", "OPS-110"],
            patch: { status: "resolved" },
          })
        }
      >
        Resolve untriaged batch
      </button>
      {toast ? (
        <div>
          <p data-testid="toast-title">{toast.title}</p>
          <button type="button" onClick={() => toast.onAction?.()}>
            {toast.actionLabel ?? "toast-action"}
          </button>
        </div>
      ) : null}
    </div>
  );
}

function renderHarness() {
  render(
    <QueryProvider>
      <IntegrationHarness />
    </QueryProvider>,
  );
}

describe("ops triage hooks integration", () => {
  it("updates the visible row set when the query changes", async () => {
    renderHarness();
    const user = userEvent.setup();

    await waitFor(() => {
      expect(screen.getByTestId("visible-ids").textContent).toContain("OPS-101");
    });

    await user.click(screen.getByRole("button", { name: "Filter investigating" }));

    await waitFor(() => {
      const visibleIds = screen.getByTestId("visible-ids").textContent ?? "";
      expect(visibleIds).toContain("OPS-101");
      expect(visibleIds).toContain("OPS-105");
      expect(visibleIds).not.toContain("OPS-102");
    });
  });

  it("keeps list and detail queries in sync after an issue mutation", async () => {
    renderHarness();
    const user = userEvent.setup();

    await waitFor(() => {
      expect(screen.getByTestId("detail-status").textContent).toBe("investigating");
    });

    await user.click(screen.getByRole("button", { name: "Resolve OPS-101" }));

    await waitFor(() => {
      expect(screen.getByTestId("toast-title").textContent).toBe("Issue updated");
      expect(screen.getByTestId("detail-status").textContent).toBe("resolved");
      expect(screen.getByTestId("status-map").textContent).toContain(
        "OPS-101:resolved",
      );
    });
  });

  it("applies a bulk mutation and updates summary counts", async () => {
    renderHarness();
    const user = userEvent.setup();

    await waitFor(() => {
      expect(screen.getByTestId("untriaged-count").textContent).toBe("3");
    });

    await user.click(screen.getByRole("button", { name: "Resolve untriaged batch" }));

    await waitFor(() => {
      expect(screen.getByTestId("toast-title").textContent).toBe(
        "Bulk update applied",
      );
      expect(screen.getByTestId("untriaged-count").textContent).toBe("0");
    });
  });

  it("rolls back a failed mutation and retries successfully", async () => {
    const consoleError = vi.spyOn(console, "error").mockImplementation(() => {});
    renderHarness();
    const user = userEvent.setup();

    configureDemoRuntime({
      failNextRequest: true,
      failureRate: 0,
      latencyMs: 0,
      mode: "stable",
    });

    await waitFor(() => {
      expect(screen.getByTestId("detail-status").textContent).toBe("investigating");
    });

    await user.click(screen.getByRole("button", { name: "Resolve OPS-101" }));

    await waitFor(() => {
      expect(screen.getByTestId("toast-title").textContent).toBe("Update failed");
      expect(screen.getByTestId("detail-status").textContent).toBe("investigating");
      expect(screen.getByTestId("status-map").textContent).toContain(
        "OPS-101:investigating",
      );
    });

    await user.click(screen.getByRole("button", { name: "Retry" }));

    await waitFor(() => {
      expect(screen.getByTestId("toast-title").textContent).toBe("Issue updated");
      expect(screen.getByTestId("detail-status").textContent).toBe("resolved");
      expect(screen.getByTestId("status-map").textContent).toContain(
        "OPS-101:resolved",
      );
    });

    consoleError.mockRestore();
  });
});
