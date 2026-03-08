import {
  type BulkIssuePatch,
  type DemoRuntimeConfig,
  type IssueLabel,
  type IssuePriority,
  type IssueQuery,
  type IssueSort,
  type IssueSource,
  type IssueStatus,
  type SavedView,
  type SlaRisk,
  type TeamRoute,
} from "@/lib/types";

export const issueStatuses: IssueStatus[] = [
  "untriaged",
  "investigating",
  "monitoring",
  "escalated",
  "resolved",
];

export const issuePriorities: IssuePriority[] = ["p0", "p1", "p2", "p3"];
export const issueSources: IssueSource[] = [
  "support",
  "qa",
  "feedback",
  "monitoring",
];
export const slaRisks: SlaRisk[] = ["healthy", "watch", "breach"];
export const issueLabels: IssueLabel[] = [
  "billing",
  "checkout",
  "latency",
  "mobile",
  "search",
  "retention",
];
export const teamRoutes: TeamRoute[] = [
  "support",
  "product",
  "payments",
  "platform",
  "growth",
];
export const issueSorts: IssueSort[] = [
  "updated_desc",
  "priority_desc",
  "sla_desc",
  "created_desc",
];

export const statusLabel: Record<IssueStatus, string> = {
  untriaged: "Untriaged",
  investigating: "Investigating",
  monitoring: "Monitoring",
  escalated: "Escalated",
  resolved: "Resolved",
};

export const priorityLabel: Record<IssuePriority, string> = {
  p0: "P0",
  p1: "P1",
  p2: "P2",
  p3: "P3",
};

export const sourceLabel: Record<IssueSource, string> = {
  support: "Support",
  qa: "QA",
  feedback: "Feedback",
  monitoring: "Monitoring",
};

export const slaRiskLabel: Record<SlaRisk, string> = {
  healthy: "Healthy",
  watch: "Watch",
  breach: "Breach",
};

export const teamRouteLabel: Record<TeamRoute, string> = {
  support: "Support",
  product: "Product",
  payments: "Payments",
  platform: "Platform",
  growth: "Growth",
};

export const issueSortLabel: Record<IssueSort, string> = {
  updated_desc: "Recently updated",
  priority_desc: "Highest priority",
  sla_desc: "Highest SLA risk",
  created_desc: "Newest first",
};

export const defaultIssueQuery: IssueQuery = {
  search: "",
  status: [],
  priority: [],
  source: [],
  slaRisk: [],
  label: [],
  sort: "updated_desc",
  page: 1,
  pageSize: 8,
};

export const defaultBulkPatch: BulkIssuePatch = {};

export const defaultDemoRuntimeConfig: DemoRuntimeConfig = {
  latencyMs: 220,
  failureRate: 0.12,
  failNextRequest: false,
  mode: "stable",
};

export const defaultSavedViews: SavedView[] = [
  {
    id: "all",
    name: "All",
    description: "Every open issue in the queue.",
    query: {},
  },
  {
    id: "at-risk",
    name: "At Risk",
    description: "Issues close to breaching SLA.",
    query: { slaRisk: ["watch", "breach"] },
  },
  {
    id: "untriaged",
    name: "Untriaged",
    description: "New items that still need triage.",
    query: { status: ["untriaged"] },
  },
  {
    id: "needs-escalation",
    name: "Needs Escalation",
    description: "High priority work that needs routing fast.",
    query: { priority: ["p0", "p1"], slaRisk: ["breach"] },
  },
];

export const priorityWeight: Record<IssuePriority, number> = {
  p0: 4,
  p1: 3,
  p2: 2,
  p3: 1,
};

export const slaWeight: Record<SlaRisk, number> = {
  breach: 3,
  watch: 2,
  healthy: 1,
};

export const storageKeys = {
  issues: "ops-triage-console:issues",
  runtime: "ops-triage-console:runtime",
};

