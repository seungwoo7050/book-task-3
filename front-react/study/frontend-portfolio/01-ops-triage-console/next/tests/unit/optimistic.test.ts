import { describe, expect, it } from "vitest";
import { createSeedIssues } from "@/lib/demo-data";
import { applyBulkPatch, applyIssuePatch } from "@/lib/optimistic";

describe("optimistic updates", () => {
  it("applies a single-issue patch and records activity", () => {
    const issue = createSeedIssues()[1];

    const nextIssue = applyIssuePatch(issue, {
      status: "resolved",
      routeTeam: "platform",
    });

    expect(nextIssue.status).toBe("resolved");
    expect(nextIssue.routeTeam).toBe("platform");
    expect(nextIssue.activity[0]?.type).toBe("route_changed");
    expect(nextIssue.activity[1]?.type).toBe("status_changed");
  });

  it("applies a bulk patch only to selected issues", () => {
    const issues = createSeedIssues();

    const nextIssues = applyBulkPatch(issues, ["OPS-102", "OPS-106"], {
      status: "resolved",
      addLabel: "billing",
    });

    const changed = nextIssues.filter((issue) =>
      ["OPS-102", "OPS-106"].includes(issue.id),
    );

    expect(changed.every((issue) => issue.status === "resolved")).toBe(true);
    expect(changed.every((issue) => issue.labels.includes("billing"))).toBe(true);
    expect(nextIssues.find((issue) => issue.id === "OPS-101")?.status).toBe(
      "investigating",
    );
  });
});
