import { randomUUID } from "node:crypto";
import Database from "better-sqlite3";
import {
  type Approval,
  type ApprovalDecision,
  type AuditLog,
  type Incident,
  type IncidentSeverity,
  type IncidentStatus,
  type StreamEvent,
  type StreamEventType,
  type UserRole
} from "../../problem/code/contracts/contracts";

interface IncidentRow {
  seq: number;
  id: string;
  title: string;
  description: string;
  severity: IncidentSeverity;
  status: IncidentStatus;
  created_by: string;
  approval_id: string | null;
  created_at: string;
  updated_at: string;
}

interface ApprovalRow {
  id: string;
  incident_id: string;
  requested_by: string;
  status: "PENDING" | "APPROVED" | "REJECTED";
  decision: ApprovalDecision | null;
  note: string | null;
  decided_by: string | null;
  decided_at: string | null;
  created_at: string;
  updated_at: string;
}

interface AuditRow {
  id: number;
  incident_id: string | null;
  actor_id: string;
  actor_role: UserRole;
  action: string;
  result: "SUCCESS" | "DENIED" | "FAILED";
  detail: string;
  created_at: string;
}

interface IdempotencyRow {
  response_status: number;
  response_body: string;
}

interface EventRow {
  id: number;
  type: StreamEventType;
  payload: string;
  created_at: string;
}

function nowIso(): string {
  return new Date().toISOString();
}

function toIncident(row: IncidentRow): Incident {
  return {
    id: row.id,
    title: row.title,
    description: row.description,
    severity: row.severity,
    status: row.status,
    createdBy: row.created_by,
    approvalId: row.approval_id,
    createdAt: row.created_at,
    updatedAt: row.updated_at
  };
}

function toApproval(row: ApprovalRow): Approval {
  return {
    id: row.id,
    incidentId: row.incident_id,
    requestedBy: row.requested_by,
    status: row.status,
    decision: row.decision,
    note: row.note,
    decidedBy: row.decided_by,
    decidedAt: row.decided_at,
    createdAt: row.created_at,
    updatedAt: row.updated_at
  };
}

function toAudit(row: AuditRow): AuditLog {
  return {
    id: row.id,
    incidentId: row.incident_id,
    actorId: row.actor_id,
    actorRole: row.actor_role,
    action: row.action,
    result: row.result,
    detail: row.detail,
    createdAt: row.created_at
  };
}

function toEvent(row: EventRow): StreamEvent {
  return {
    eventId: row.id,
    type: row.type,
    timestamp: row.created_at,
    payload: JSON.parse(row.payload)
  };
}

export class IncidentOpsStore {
  private readonly db: Database.Database;

  constructor(path = ":memory:") {
    this.db = new Database(path);
    this.initialize();
  }

  close(): void {
    this.db.close();
  }

  createIncident(input: {
    title: string;
    description: string;
    severity: IncidentSeverity;
    createdBy: string;
  }): Incident {
    const id = randomUUID();
    const now = nowIso();

    this.db.prepare(
      `INSERT INTO incidents (
        id, title, description, severity, status, created_by, approval_id, created_at, updated_at
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`
    ).run(
      id,
      input.title,
      input.description,
      input.severity,
      "OPEN",
      input.createdBy,
      null,
      now,
      now
    );

    return this.getIncident(id) as Incident;
  }

  getIncident(id: string): Incident | null {
    const row = this.db
      .prepare("SELECT seq, id, title, description, severity, status, created_by, approval_id, created_at, updated_at FROM incidents WHERE id = ?")
      .get(id) as IncidentRow | undefined;

    if (!row) {
      return null;
    }

    return toIncident(row);
  }

  listIncidents(cursor: number | null, limit: number): { incidents: Incident[]; nextCursor: string | null } {
    const rows = (cursor
      ? this.db
          .prepare(
            "SELECT seq, id, title, description, severity, status, created_by, approval_id, created_at, updated_at FROM incidents WHERE seq < ? ORDER BY seq DESC LIMIT ?"
          )
          .all(cursor, limit)
      : this.db
          .prepare(
            "SELECT seq, id, title, description, severity, status, created_by, approval_id, created_at, updated_at FROM incidents ORDER BY seq DESC LIMIT ?"
          )
          .all(limit)) as IncidentRow[];

    const incidents = rows.map(toIncident);
    const nextCursor = rows.length === limit ? String(rows[rows.length - 1].seq) : null;

    return { incidents, nextCursor };
  }

  updateIncidentStatus(id: string, status: IncidentStatus, approvalId: string | null = null): Incident {
    const now = nowIso();
    this.db
      .prepare("UPDATE incidents SET status = ?, approval_id = ?, updated_at = ? WHERE id = ?")
      .run(status, approvalId, now, id);

    return this.getIncident(id) as Incident;
  }

  createApproval(input: {
    incidentId: string;
    requestedBy: string;
    reason: string;
  }): Approval {
    const id = randomUUID();
    const now = nowIso();

    this.db
      .prepare(
        `INSERT INTO approvals (
          id, incident_id, requested_by, status, decision, note, decided_by, decided_at, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
      )
      .run(id, input.incidentId, input.requestedBy, "PENDING", null, input.reason, null, null, now, now);

    return this.getApproval(id) as Approval;
  }

  getApproval(id: string): Approval | null {
    const row = this.db
      .prepare(
        "SELECT id, incident_id, requested_by, status, decision, note, decided_by, decided_at, created_at, updated_at FROM approvals WHERE id = ?"
      )
      .get(id) as ApprovalRow | undefined;

    if (!row) {
      return null;
    }

    return toApproval(row);
  }

  updateApprovalDecision(input: {
    id: string;
    decision: ApprovalDecision;
    note: string | null;
    decidedBy: string;
  }): Approval {
    const status = input.decision === "APPROVE" ? "APPROVED" : "REJECTED";
    const now = nowIso();

    this.db
      .prepare(
        "UPDATE approvals SET status = ?, decision = ?, note = ?, decided_by = ?, decided_at = ?, updated_at = ? WHERE id = ?"
      )
      .run(status, input.decision, input.note, input.decidedBy, now, now, input.id);

    return this.getApproval(input.id) as Approval;
  }

  addAudit(input: {
    incidentId: string | null;
    actorId: string;
    actorRole: UserRole;
    action: string;
    result: "SUCCESS" | "DENIED" | "FAILED";
    detail: string;
  }): AuditLog {
    const now = nowIso();
    const result = this.db
      .prepare(
        "INSERT INTO audit_logs (incident_id, actor_id, actor_role, action, result, detail, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)"
      )
      .run(input.incidentId, input.actorId, input.actorRole, input.action, input.result, input.detail, now);

    const row = this.db
      .prepare(
        "SELECT id, incident_id, actor_id, actor_role, action, result, detail, created_at FROM audit_logs WHERE id = ?"
      )
      .get(Number(result.lastInsertRowid)) as AuditRow;

    return toAudit(row);
  }

  listAudit(incidentId: string | null): AuditLog[] {
    const rows = (incidentId
      ? this.db
          .prepare(
            "SELECT id, incident_id, actor_id, actor_role, action, result, detail, created_at FROM audit_logs WHERE incident_id = ? ORDER BY id ASC"
          )
          .all(incidentId)
      : this.db
          .prepare(
            "SELECT id, incident_id, actor_id, actor_role, action, result, detail, created_at FROM audit_logs ORDER BY id ASC"
          )
          .all()) as AuditRow[];

    return rows.map(toAudit);
  }

  appendEvent(type: StreamEventType, payload: unknown): StreamEvent {
    const now = nowIso();
    const result = this.db
      .prepare("INSERT INTO stream_events (type, payload, created_at) VALUES (?, ?, ?)")
      .run(type, JSON.stringify(payload), now);

    const row = this.db
      .prepare("SELECT id, type, payload, created_at FROM stream_events WHERE id = ?")
      .get(Number(result.lastInsertRowid)) as EventRow;

    return toEvent(row);
  }

  listEventsSince(lastEventId: number): StreamEvent[] {
    const rows = this.db
      .prepare("SELECT id, type, payload, created_at FROM stream_events WHERE id > ? ORDER BY id ASC")
      .all(lastEventId) as EventRow[];

    return rows.map(toEvent);
  }

  getIdempotent(scope: string, idempotencyKey: string): { status: number; body: unknown } | null {
    const row = this.db
      .prepare(
        "SELECT response_status, response_body FROM idempotency_records WHERE scope = ? AND idempotency_key = ?"
      )
      .get(scope, idempotencyKey) as IdempotencyRow | undefined;

    if (!row) {
      return null;
    }

    return {
      status: row.response_status,
      body: JSON.parse(row.response_body)
    };
  }

  saveIdempotent(scope: string, idempotencyKey: string, status: number, body: unknown): void {
    const now = nowIso();
    this.db
      .prepare(
        "INSERT OR REPLACE INTO idempotency_records (scope, idempotency_key, response_status, response_body, created_at) VALUES (?, ?, ?, ?, ?)"
      )
      .run(scope, idempotencyKey, status, JSON.stringify(body), now);
  }

  private initialize(): void {
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS incidents (
        seq INTEGER PRIMARY KEY AUTOINCREMENT,
        id TEXT NOT NULL UNIQUE,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        severity TEXT NOT NULL,
        status TEXT NOT NULL,
        created_by TEXT NOT NULL,
        approval_id TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
      );

      CREATE TABLE IF NOT EXISTS approvals (
        id TEXT PRIMARY KEY,
        incident_id TEXT NOT NULL,
        requested_by TEXT NOT NULL,
        status TEXT NOT NULL,
        decision TEXT,
        note TEXT,
        decided_by TEXT,
        decided_at TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
      );

      CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        incident_id TEXT,
        actor_id TEXT NOT NULL,
        actor_role TEXT NOT NULL,
        action TEXT NOT NULL,
        result TEXT NOT NULL,
        detail TEXT NOT NULL,
        created_at TEXT NOT NULL
      );

      CREATE TABLE IF NOT EXISTS stream_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        payload TEXT NOT NULL,
        created_at TEXT NOT NULL
      );

      CREATE TABLE IF NOT EXISTS idempotency_records (
        scope TEXT NOT NULL,
        idempotency_key TEXT NOT NULL,
        response_status INTEGER NOT NULL,
        response_body TEXT NOT NULL,
        created_at TEXT NOT NULL,
        PRIMARY KEY (scope, idempotency_key)
      );
    `);
  }
}
