import { createServer, type IncomingMessage, type ServerResponse } from "node:http";
import { randomUUID } from "node:crypto";
import { WebSocketServer, type WebSocket } from "ws";
import {
  USER_ROLES,
  type Approval,
  type AuthActor,
  type Incident,
  type LoginResponse,
  type StreamEvent,
  type UserRole
} from "../../problem/code/contracts/contracts";
import { HttpError, assertFound } from "./errors";
import {
  parseApprovalDecision,
  parseCreateIncidentRequest,
  parseLoginRequest,
  parsePagination,
  parseRequestResolution
} from "./validation";
import { IncidentOpsStore } from "./store";

interface StructuredLog {
  level: "info" | "error";
  method: string;
  path: string;
  status: number;
  latencyMs: number;
  traceId: string;
  detail: string;
}

export interface IncidentOpsServerOptions {
  port?: number;
  dbPath?: string;
  onStructuredLog?: (entry: StructuredLog) => void;
}

export interface IncidentOpsServerHandle {
  readonly port: number;
  readonly url: string;
  readonly store: IncidentOpsStore;
  readonly structuredLogs: StructuredLog[];
  stop: () => Promise<void>;
}

function nowIso(): string {
  return new Date().toISOString();
}

function issueToken(actor: AuthActor): string {
  return Buffer.from(JSON.stringify(actor), "utf8").toString("base64url");
}

function parseToken(token: string): AuthActor {
  const decoded = Buffer.from(token, "base64url").toString("utf8");
  const parsed = JSON.parse(decoded) as Partial<AuthActor>;

  if (!parsed.userId || !parsed.role || !USER_ROLES.includes(parsed.role as UserRole)) {
    throw new Error("invalid token");
  }

  return {
    userId: parsed.userId,
    role: parsed.role as UserRole
  };
}

async function readBody(req: IncomingMessage): Promise<unknown> {
  const chunks: Buffer[] = [];

  for await (const chunk of req) {
    chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
  }

  if (chunks.length === 0) {
    return {};
  }

  const text = Buffer.concat(chunks).toString("utf8");
  return JSON.parse(text);
}

function sendJson(res: ServerResponse, status: number, body: unknown): void {
  res.statusCode = status;
  res.setHeader("content-type", "application/json");
  res.end(JSON.stringify(body));
}

function getPathParts(pathname: string): string[] {
  return pathname
    .split("/")
    .map(part => part.trim())
    .filter(Boolean);
}

function authFromRequest(req: IncomingMessage): AuthActor {
  const raw = req.headers.authorization;
  if (!raw?.startsWith("Bearer ")) {
    throw new HttpError(401, "missing bearer token");
  }

  const token = raw.slice("Bearer ".length);
  try {
    return parseToken(token);
  } catch (_error) {
    throw new HttpError(401, "invalid bearer token");
  }
}

function requireRole(
  actor: AuthActor,
  allowed: UserRole[],
  options: {
    store: IncidentOpsStore;
    action: string;
    incidentId: string | null;
  }
): void {
  if (allowed.includes(actor.role)) {
    return;
  }

  options.store.addAudit({
    incidentId: options.incidentId,
    actorId: actor.userId,
    actorRole: actor.role,
    action: options.action,
    result: "DENIED",
    detail: `role ${actor.role} is not allowed`
  });

  throw new HttpError(403, "forbidden role");
}

export async function startIncidentOpsServer(
  options: IncidentOpsServerOptions = {}
): Promise<IncidentOpsServerHandle> {
  const store = new IncidentOpsStore(options.dbPath ?? ":memory:");
  const structuredLogs: StructuredLog[] = [];
  const clients = new Set<WebSocket>();

  const wsServer = new WebSocketServer({ noServer: true });

  const broadcastEvent = (event: StreamEvent): void => {
    const payload = JSON.stringify(event);
    for (const client of clients) {
      if (client.readyState === client.OPEN) {
        client.send(payload);
      }
    }
  };

  wsServer.on("connection", (socket, req) => {
    clients.add(socket);

    const url = new URL(req.url ?? "/ws", "http://localhost");
    const lastEventId = Number(url.searchParams.get("lastEventId") ?? "0");
    const replayBase = Number.isFinite(lastEventId) && lastEventId >= 0 ? lastEventId : 0;

    const replayEvents = store.listEventsSince(replayBase);
    for (const event of replayEvents) {
      socket.send(JSON.stringify(event));
    }

    socket.on("close", () => {
      clients.delete(socket);
    });
  });

  const server = createServer(async (req, res) => {
    const startedAt = Date.now();
    const traceId = randomUUID();
    const method = req.method ?? "GET";
    const url = new URL(req.url ?? "/", "http://localhost");
    const pathname = url.pathname;
    let status = 200;
    let detail = "ok";

    try {
      const idempotencyHeader = req.headers["x-idempotency-key"];
      const idempotencyKey = typeof idempotencyHeader === "string" && idempotencyHeader.trim() ? idempotencyHeader : null;
      const idempotencyScope = `${method} ${pathname}`;

      const respond = (responseStatus: number, body: unknown): void => {
        status = responseStatus;
        if (idempotencyKey && responseStatus < 500) {
          store.saveIdempotent(idempotencyScope, idempotencyKey, responseStatus, body);
        }
        sendJson(res, responseStatus, body);
      };

      if (idempotencyKey) {
        const cached = store.getIdempotent(idempotencyScope, idempotencyKey);
        if (cached) {
          status = cached.status;
          sendJson(res, cached.status, cached.body);
          return;
        }
      }

      if (method === "POST" && pathname === "/auth/login") {
        const payload = await readBody(req);
        const parsed = parseLoginRequest(payload);

        const actor: AuthActor = {
          userId: parsed.userId,
          role: parsed.role
        };

        const response: LoginResponse = {
          token: issueToken(actor),
          actor
        };

        respond(200, response);
        return;
      }

      const actor = authFromRequest(req);

      if (method === "POST" && pathname === "/incidents") {
        requireRole(actor, ["REPORTER", "OPERATOR"], {
          store,
          action: "incident.create",
          incidentId: null
        });

        const payload = await readBody(req);
        const parsed = parseCreateIncidentRequest(payload);
        const incident = store.createIncident({
          title: parsed.title,
          description: parsed.description ?? "",
          severity: parsed.severity,
          createdBy: actor.userId
        });

        store.addAudit({
          incidentId: incident.id,
          actorId: actor.userId,
          actorRole: actor.role,
          action: "incident.create",
          result: "SUCCESS",
          detail: `created incident ${incident.id}`
        });

        const event = store.appendEvent("incident.created", incident);
        broadcastEvent(event);

        respond(201, { incident, eventId: event.eventId });
        return;
      }

      if (method === "GET" && pathname === "/incidents") {
        const { cursor, limit } = parsePagination(url.searchParams.get("cursor"), url.searchParams.get("limit"));
        const result = store.listIncidents(cursor, limit);
        respond(200, result);
        return;
      }

      if (method === "GET" && pathname === "/audit") {
        const incidentId = url.searchParams.get("incidentId");
        const items = store.listAudit(incidentId);
        respond(200, { items });
        return;
      }

      const parts = getPathParts(pathname);

      if (method === "POST" && parts.length === 3 && parts[0] === "incidents" && parts[2] === "ack") {
        const incidentId = parts[1];
        requireRole(actor, ["OPERATOR"], {
          store,
          action: "incident.ack",
          incidentId
        });

        const incident = assertFound(store.getIncident(incidentId), "incident not found");
        if (incident.status !== "OPEN") {
          throw new HttpError(409, `cannot ack incident in status ${incident.status}`);
        }

        const updated = store.updateIncidentStatus(incidentId, "ACKED");
        store.addAudit({
          incidentId,
          actorId: actor.userId,
          actorRole: actor.role,
          action: "incident.ack",
          result: "SUCCESS",
          detail: `acked incident ${incidentId}`
        });

        const event = store.appendEvent("incident.updated", updated);
        broadcastEvent(event);

        respond(200, { incident: updated, eventId: event.eventId });
        return;
      }

      if (
        method === "POST" &&
        parts.length === 3 &&
        parts[0] === "incidents" &&
        parts[2] === "request-resolution"
      ) {
        const incidentId = parts[1];
        requireRole(actor, ["OPERATOR"], {
          store,
          action: "incident.request_resolution",
          incidentId
        });

        const payload = await readBody(req);
        const parsed = parseRequestResolution(payload);
        const incident = assertFound(store.getIncident(incidentId), "incident not found");

        if (incident.status !== "ACKED") {
          throw new HttpError(409, "resolution request requires ACKED incident");
        }

        const approval = store.createApproval({
          incidentId,
          requestedBy: actor.userId,
          reason: parsed.reason
        });

        const updated = store.updateIncidentStatus(incidentId, "RESOLUTION_PENDING", approval.id);

        store.addAudit({
          incidentId,
          actorId: actor.userId,
          actorRole: actor.role,
          action: "incident.request_resolution",
          result: "SUCCESS",
          detail: `approval ${approval.id} requested`
        });

        const approvalEvent = store.appendEvent("approval.requested", approval);
        const incidentEvent = store.appendEvent("incident.updated", updated);
        broadcastEvent(approvalEvent);
        broadcastEvent(incidentEvent);

        respond(200, {
          incident: updated,
          approval,
          eventId: incidentEvent.eventId
        });
        return;
      }

      if (method === "POST" && parts.length === 3 && parts[0] === "approvals" && parts[2] === "decision") {
        const approvalId = parts[1];
        requireRole(actor, ["APPROVER"], {
          store,
          action: "approval.decide",
          incidentId: null
        });

        const payload = await readBody(req);
        const parsed = parseApprovalDecision(payload);
        const approval = assertFound(store.getApproval(approvalId), "approval not found");

        if (approval.status !== "PENDING") {
          throw new HttpError(409, `approval already ${approval.status}`);
        }

        const decided = store.updateApprovalDecision({
          id: approvalId,
          decision: parsed.decision,
          note: parsed.note ?? null,
          decidedBy: actor.userId
        });

        const incidentStatus = parsed.decision === "APPROVE" ? "RESOLVED" : "ACKED";
        const updatedIncident = store.updateIncidentStatus(decided.incidentId, incidentStatus, approvalId);

        store.addAudit({
          incidentId: decided.incidentId,
          actorId: actor.userId,
          actorRole: actor.role,
          action: "approval.decide",
          result: "SUCCESS",
          detail: `approval ${approvalId} -> ${parsed.decision}`
        });

        const approvalEvent = store.appendEvent("approval.decided", decided);
        const incidentEvent = store.appendEvent("incident.updated", updatedIncident);
        broadcastEvent(approvalEvent);
        broadcastEvent(incidentEvent);

        respond(200, {
          incident: updatedIncident,
          approval: decided,
          eventId: incidentEvent.eventId
        });
        return;
      }

      throw new HttpError(404, "route not found");
    } catch (error) {
      if (error instanceof HttpError) {
        status = error.status;
        detail = error.detail;
        sendJson(res, error.status, {
          error: error.detail,
          traceId,
          at: nowIso()
        });
      } else if (error instanceof SyntaxError) {
        status = 400;
        detail = "invalid json payload";
        sendJson(res, 400, {
          error: "invalid json payload",
          traceId,
          at: nowIso()
        });
      } else {
        status = 500;
        detail = error instanceof Error ? error.message : "internal server error";
        sendJson(res, 500, {
          error: "internal server error",
          detail,
          traceId,
          at: nowIso()
        });
      }
    } finally {
      const entry: StructuredLog = {
        level: status >= 500 ? "error" : "info",
        method,
        path: pathname,
        status,
        latencyMs: Date.now() - startedAt,
        traceId,
        detail
      };

      structuredLogs.push(entry);
      options.onStructuredLog?.(entry);
    }
  });

  server.on("upgrade", (req, socket, head) => {
    const url = new URL(req.url ?? "/", "http://localhost");
    if (url.pathname !== "/ws") {
      socket.destroy();
      return;
    }

    wsServer.handleUpgrade(req, socket, head, client => {
      wsServer.emit("connection", client, req);
    });
  });

  const port = await new Promise<number>((resolve, reject) => {
    const desiredPort = options.port ?? 0;
    server.once("error", reject);
    server.listen(desiredPort, () => {
      const address = server.address();
      if (!address || typeof address === "string") {
        reject(new Error("failed to bind server"));
        return;
      }
      resolve(address.port);
    });
  });

  return {
    port,
    url: `http://127.0.0.1:${port}`,
    store,
    structuredLogs,
    stop: async () => {
      for (const client of clients) {
        client.close();
      }
      await new Promise<void>((resolve, reject) => {
        server.close(error => {
          if (error) {
            reject(error);
            return;
          }
          resolve();
        });
      });
      store.close();
    }
  };
}
