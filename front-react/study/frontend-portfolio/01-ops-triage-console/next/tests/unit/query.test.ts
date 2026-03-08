import { describe, expect, it } from "vitest";
import { defaultIssueQuery, defaultSavedViews } from "@/lib/constants";
import { createSeedIssues } from "@/lib/demo-data";
import {
  applyIssueQuery,
  createDashboardSummary,
  mergeSavedView,
  serializeSavedView,
} from "@/lib/query";

describe("query helpers", () => {
  it("filters issues by status and search text", () => {
    const issues = createSeedIssues();

    const result = applyIssueQuery(issues, {
      ...defaultIssueQuery,
      status: ["untriaged"],
      search: "feedback",
    });

    expect(result.items.map((issue) => issue.id)).toEqual(["OPS-102", "OPS-106"]);
    expect(result.total).toBe(2);
  });

  it("sorts the queue by priority descending", () => {
    const issues = createSeedIssues();

    const result = applyIssueQuery(issues, {
      ...defaultIssueQuery,
      sort: "priority_desc",
    });

    expect(result.items[0]?.id).toBe("OPS-101");
    expect(result.items[1]?.id).toBe("OPS-111");
  });

  it("merges a saved view and resets pagination", () => {
    const result = mergeSavedView(
      {
        ...defaultIssueQuery,
        page: 3,
        search: "wallet",
      },
      defaultSavedViews[1],
    );

    expect(result.page).toBe(1);
    expect(result.search).toBe("wallet");
    expect(result.slaRisk).toEqual(["watch", "breach"]);
  });

  it("serializes only the stable saved-view payload", () => {
    expect(serializeSavedView(defaultSavedViews[2])).toBe(
      JSON.stringify({
        id: "untriaged",
        query: { status: ["untriaged"] },
      }),
    );
  });

  it("builds dashboard summary counters from seeded issues", () => {
    const summary = createDashboardSummary(createSeedIssues());

    expect(summary.totalIssues).toBe(12);
    expect(summary.untriagedCount).toBe(3);
    expect(summary.atRiskCount).toBe(8);
    expect(summary.priorityCounts.p0).toBe(2);
    expect(summary.sourceCounts.monitoring).toBe(3);
  });
});
