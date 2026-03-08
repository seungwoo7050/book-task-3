export const USER_ROLES = ["REPORTER", "OPERATOR", "APPROVER"] as const;
export type UserRole = (typeof USER_ROLES)[number];

export const INCIDENT_SEVERITIES = ["P1", "P2", "P3"] as const;
export type IncidentSeverity = (typeof INCIDENT_SEVERITIES)[number];

export const INCIDENT_STATUSES = [
  "OPEN",
  "ACKED",
  "RESOLUTION_PENDING",
  "RESOLVED",
] as const;
export type IncidentStatus = (typeof INCIDENT_STATUSES)[number];

export const APPROVAL_DECISIONS = ["APPROVE", "REJECT"] as const;
export type ApprovalDecision = (typeof APPROVAL_DECISIONS)[number];

export const STREAM_EVENT_TYPES = [
  "incident.created",
  "incident.updated",
  "approval.requested",
  "approval.decided",
] as const;
export type StreamEventType = (typeof STREAM_EVENT_TYPES)[number];

export const QUEUE_JOB_STATES = ["pending", "synced", "failed"] as const;
export type QueueJobState = (typeof QUEUE_JOB_STATES)[number];

export type QueueAction =
  | "POST /incidents"
  | "POST /incidents/:id/ack"
  | "POST /incidents/:id/request-resolution"
  | "POST /approvals/:id/decision";

export interface AuthActor {
  userId: string;
  role: UserRole;
}

export interface Incident {
  id: string;
  title: string;
  description: string;
  severity: IncidentSeverity;
  status: IncidentStatus;
  createdBy: string;
  approvalId: string | null;
  createdAt: string;
  updatedAt: string;
}

export interface Approval {
  id: string;
  incidentId: string;
  requestedBy: string;
  status: "PENDING" | "APPROVED" | "REJECTED";
  decision: ApprovalDecision | null;
  note: string | null;
  decidedBy: string | null;
  decidedAt: string | null;
  createdAt: string;
  updatedAt: string;
}

export interface AuditLog {
  id: number;
  incidentId: string | null;
  actorId: string;
  actorRole: UserRole;
  action: string;
  result: "SUCCESS" | "DENIED" | "FAILED";
  detail: string;
  createdAt: string;
}

export interface StreamEvent<TPayload = unknown> {
  eventId: number;
  type: StreamEventType;
  timestamp: string;
  payload: TPayload;
}

export interface QueueJob {
  id: string;
  action: QueueAction;
  payload: Record<string, unknown>;
  idempotencyKey: string;
  attempts: number;
  state: QueueJobState;
  lastError: string | null;
}

export interface LoginRequest {
  userId: string;
  role: UserRole;
}

export interface LoginResponse {
  token: string;
  actor: AuthActor;
}

export interface CreateIncidentRequest {
  title: string;
  description?: string;
  severity: IncidentSeverity;
}

export interface RequestResolutionBody {
  reason: string;
}

export interface ApprovalDecisionBody {
  decision: ApprovalDecision;
  note?: string;
}
