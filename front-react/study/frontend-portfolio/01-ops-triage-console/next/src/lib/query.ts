import {
  defaultIssueQuery,
  priorityWeight,
  slaWeight,
} from "@/lib/constants";
import {
  type DashboardSummary,
  type Issue,
  type IssueListResult,
  type IssuePriority,
  type IssueQuery,
  type IssueSource,
  type SavedView,
} from "@/lib/types";

export function mergeSavedView(query: IssueQuery, view: SavedView): IssueQuery {
  return {
    ...defaultIssueQuery,
    ...query,
    ...view.query,
    page: 1,
  };
}

export function serializeSavedView(view: SavedView): string {
  return JSON.stringify({
    id: view.id,
    query: view.query,
  });
}

export function applyIssueQuery(issues: Issue[], query: IssueQuery): IssueListResult {
  const filtered = issues.filter((issue) => {
    const matchesSearch =
      query.search.trim().length === 0 ||
      `${issue.title} ${issue.summary} ${issue.customer} ${issue.routeTeam} ${issue.labels.join(" ")}`
        .toLowerCase()
        .includes(query.search.toLowerCase());

    const matchesStatus =
      query.status.length === 0 || query.status.includes(issue.status);
    const matchesPriority =
      query.priority.length === 0 || query.priority.includes(issue.priority);
    const matchesSource =
      query.source.length === 0 || query.source.includes(issue.source);
    const matchesSla =
      query.slaRisk.length === 0 || query.slaRisk.includes(issue.slaRisk);
    const matchesLabel =
      query.label.length === 0 ||
      query.label.every((label) => issue.labels.includes(label));

    return (
      matchesSearch &&
      matchesStatus &&
      matchesPriority &&
      matchesSource &&
      matchesSla &&
      matchesLabel
    );
  });

  const sorted = [...filtered].sort((left, right) => {
    switch (query.sort) {
      case "priority_desc":
        return priorityWeight[right.priority] - priorityWeight[left.priority];
      case "sla_desc":
        return slaWeight[right.slaRisk] - slaWeight[left.slaRisk];
      case "created_desc":
        return (
          new Date(right.createdAt).getTime() - new Date(left.createdAt).getTime()
        );
      case "updated_desc":
      default:
        return (
          new Date(right.updatedAt).getTime() - new Date(left.updatedAt).getTime()
        );
    }
  });

  const start = (query.page - 1) * query.pageSize;
  const end = start + query.pageSize;

  return {
    items: sorted.slice(start, end),
    total: sorted.length,
    page: query.page,
    pageSize: query.pageSize,
    totalPages: Math.max(1, Math.ceil(sorted.length / query.pageSize)),
  };
}

export function createDashboardSummary(issues: Issue[]): DashboardSummary {
  const priorityCounts: Record<IssuePriority, number> = {
    p0: 0,
    p1: 0,
    p2: 0,
    p3: 0,
  };

  const sourceCounts: Record<IssueSource, number> = {
    support: 0,
    qa: 0,
    feedback: 0,
    monitoring: 0,
  };

  for (const issue of issues) {
    priorityCounts[issue.priority] += 1;
    sourceCounts[issue.source] += 1;
  }

  const atRiskCount = issues.filter(
    (issue) => issue.slaRisk === "watch" || issue.slaRisk === "breach",
  ).length;
  const untriagedCount = issues.filter(
    (issue) => issue.status === "untriaged",
  ).length;
  const escalatedCount = issues.filter(
    (issue) => issue.status === "escalated",
  ).length;

  const changedLastDay = issues.filter((issue) => {
    return Date.now() - new Date(issue.updatedAt).getTime() < 86_400_000;
  }).length;

  return {
    totalIssues: issues.length,
    atRiskCount,
    untriagedCount,
    escalatedCount,
    priorityCounts,
    sourceCounts,
    recentChanges: [
      {
        label: "Changed in 24h",
        value: `${changedLastDay}`,
        tone: changedLastDay > 4 ? "warning" : "neutral",
      },
      {
        label: "Breach risk",
        value: `${issues.filter((issue) => issue.slaRisk === "breach").length}`,
        tone:
          issues.filter((issue) => issue.slaRisk === "breach").length > 0
            ? "danger"
            : "success",
      },
      {
        label: "Resolved this sweep",
        value: `${issues.filter((issue) => issue.status === "resolved").length}`,
        tone: "success",
      },
    ],
  };
}

