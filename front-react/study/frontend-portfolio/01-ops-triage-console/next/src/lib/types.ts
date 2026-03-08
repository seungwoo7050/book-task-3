export type IssueStatus =
  | "untriaged"
  | "investigating"
  | "monitoring"
  | "escalated"
  | "resolved";

export type IssuePriority = "p0" | "p1" | "p2" | "p3";
export type IssueSource = "support" | "qa" | "feedback" | "monitoring";
export type SlaRisk = "healthy" | "watch" | "breach";
export type IssueLabel =
  | "billing"
  | "checkout"
  | "latency"
  | "mobile"
  | "search"
  | "retention";
export type TeamRoute =
  | "support"
  | "product"
  | "payments"
  | "platform"
  | "growth";
export type AccountTier = "starter" | "growth" | "enterprise";
export type IssueSort =
  | "updated_desc"
  | "priority_desc"
  | "sla_desc"
  | "created_desc";

export interface IssueActivity {
  id: string;
  type:
    | "created"
    | "status_changed"
    | "priority_changed"
    | "label_changed"
    | "route_changed"
    | "note_added"
    | "bulk_updated";
  actor: string;
  message: string;
  timestamp: string;
}

export interface Issue {
  id: string;
  title: string;
  summary: string;
  customer: string;
  source: IssueSource;
  status: IssueStatus;
  priority: IssuePriority;
  slaRisk: SlaRisk;
  labels: IssueLabel[];
  routeTeam: TeamRoute;
  owner: string;
  accountTier: AccountTier;
  affectedUsers: number;
  createdAt: string;
  updatedAt: string;
  lastSeenAt: string;
  operatorNote: string;
  activity: IssueActivity[];
}

export interface IssueQuery {
  search: string;
  status: IssueStatus[];
  priority: IssuePriority[];
  source: IssueSource[];
  slaRisk: SlaRisk[];
  label: IssueLabel[];
  sort: IssueSort;
  page: number;
  pageSize: number;
}

export interface IssuePatch {
  status?: IssueStatus;
  priority?: IssuePriority;
  labels?: IssueLabel[];
  routeTeam?: TeamRoute;
  operatorNote?: string;
}

export interface BulkIssuePatch {
  status?: IssueStatus;
  priority?: IssuePriority;
  addLabel?: IssueLabel;
  routeTeam?: TeamRoute;
}

export interface SavedView {
  id: string;
  name: string;
  description: string;
  query: Partial<IssueQuery>;
}

export interface DashboardSummary {
  totalIssues: number;
  atRiskCount: number;
  untriagedCount: number;
  escalatedCount: number;
  priorityCounts: Record<IssuePriority, number>;
  sourceCounts: Record<IssueSource, number>;
  recentChanges: Array<{
    label: string;
    value: string;
    tone: "neutral" | "success" | "warning" | "danger";
  }>;
}

export interface IssueListResult {
  items: Issue[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

export interface DemoRuntimeConfig {
  latencyMs: number;
  failureRate: number;
  failNextRequest: boolean;
  mode: "stable" | "chaos";
}

export interface DemoServiceError extends Error {
  code: "DEMO_TRANSIENT_FAILURE";
  retryable: true;
}

