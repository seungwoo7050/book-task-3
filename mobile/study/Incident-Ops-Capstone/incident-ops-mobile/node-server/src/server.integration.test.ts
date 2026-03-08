import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { WebSocket } from "ws";
import { startIncidentOpsServer, type IncidentOpsServerHandle } from "./server";

let server: IncidentOpsServerHandle;

async function login(role: "REPORTER" | "OPERATOR" | "APPROVER", userId: string): Promise<string> {
  const response = await fetch(`${server.url}/auth/login`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ role, userId })
  });

  expect(response.status).toBe(200);
  const body = (await response.json()) as { token: string };
  return body.token;
}

async function authed<T>(input: {
  token: string;
  method: "GET" | "POST";
  path: string;
  body?: unknown;
  idempotencyKey?: string;
  expectedStatus?: number;
}): Promise<T> {
  const response = await fetch(`${server.url}${input.path}`, {
    method: input.method,
    headers: {
      authorization: `Bearer ${input.token}`,
      "content-type": "application/json",
      ...(input.idempotencyKey ? { "x-idempotency-key": input.idempotencyKey } : {})
    },
    body: input.body ? JSON.stringify(input.body) : undefined
  });

  expect(response.status).toBe(input.expectedStatus ?? 200);
  return (await response.json()) as T;
}

describe("incident ops server", () => {
  beforeEach(async () => {
    server = await startIncidentOpsServer();
  });

  afterEach(async () => {
    await server.stop();
  });

  it("runs approval approve flow and writes audit logs", async () => {
    const reporter = await login("REPORTER", "reporter.test");
    const operator = await login("OPERATOR", "operator.test");
    const approver = await login("APPROVER", "approver.test");

    const created = await authed<{
      incident: { id: string; status: string };
      eventId: number;
    }>({
      token: reporter,
      method: "POST",
      path: "/incidents",
      body: {
        title: "Server flow incident",
        severity: "P1",
        description: "created from integration test"
      },
      expectedStatus: 201,
      idempotencyKey: "create-1"
    });

    const acked = await authed<{
      incident: { id: string; status: string };
    }>({
      token: operator,
      method: "POST",
      path: `/incidents/${created.incident.id}/ack`,
      idempotencyKey: "ack-1"
    });

    expect(acked.incident.status).toBe("ACKED");

    const requested = await authed<{
      incident: { status: string };
      approval: { id: string; status: string };
    }>({
      token: operator,
      method: "POST",
      path: `/incidents/${created.incident.id}/request-resolution`,
      body: { reason: "mitigated" },
      idempotencyKey: "resolution-1"
    });

    expect(requested.incident.status).toBe("RESOLUTION_PENDING");
    expect(requested.approval.status).toBe("PENDING");

    const decided = await authed<{
      incident: { status: string };
      approval: { status: string };
    }>({
      token: approver,
      method: "POST",
      path: `/approvals/${requested.approval.id}/decision`,
      body: { decision: "APPROVE", note: "ok" },
      idempotencyKey: "decision-1"
    });

    expect(decided.incident.status).toBe("RESOLVED");
    expect(decided.approval.status).toBe("APPROVED");

    const audit = await authed<{ items: Array<{ action: string }> }>({
      token: approver,
      method: "GET",
      path: `/audit?incidentId=${created.incident.id}`
    });

    const actions = audit.items.map(item => item.action);
    expect(actions).toContain("incident.create");
    expect(actions).toContain("incident.ack");
    expect(actions).toContain("incident.request_resolution");
    expect(actions).toContain("approval.decide");
  });

  it("returns ACKED when approval is rejected", async () => {
    const reporter = await login("REPORTER", "reporter.reject");
    const operator = await login("OPERATOR", "operator.reject");
    const approver = await login("APPROVER", "approver.reject");

    const created = await authed<{ incident: { id: string } }>({
      token: reporter,
      method: "POST",
      path: "/incidents",
      body: { title: "reject me", severity: "P3" },
      expectedStatus: 201
    });

    await authed({
      token: operator,
      method: "POST",
      path: `/incidents/${created.incident.id}/ack`
    });

    const request = await authed<{ approval: { id: string } }>({
      token: operator,
      method: "POST",
      path: `/incidents/${created.incident.id}/request-resolution`,
      body: { reason: "request reject path" }
    });

    const decision = await authed<{ incident: { status: string } }>({
      token: approver,
      method: "POST",
      path: `/approvals/${request.approval.id}/decision`,
      body: { decision: "REJECT", note: "not enough proof" }
    });

    expect(decision.incident.status).toBe("ACKED");
  });

  it("replays websocket events from lastEventId", async () => {
    const reporter = await login("REPORTER", "reporter.ws");

    const replayAll = await new Promise<Array<{ eventId: number; type: string }>>((resolve, reject) => {
      const socket = new WebSocket(`${server.url.replace("http", "ws")}/ws?lastEventId=0`);
      const events: Array<{ eventId: number; type: string }> = [];

      const timeout = setTimeout(() => {
        socket.close();
        reject(new Error("timeout while waiting for initial replay"));
      }, 4000);

      socket.on("message", payload => {
        events.push(JSON.parse(payload.toString()) as { eventId: number; type: string });
        if (events.length >= 1) {
          clearTimeout(timeout);
          socket.close();
          resolve(events);
        }
      });

      socket.on("error", error => {
        clearTimeout(timeout);
        reject(error);
      });

      void authed({
        token: reporter,
        method: "POST",
        path: "/incidents",
        body: { title: "ws one", severity: "P2" },
        expectedStatus: 201
      });
    });

    const lastSeen = replayAll[replayAll.length - 1]?.eventId ?? 0;

    await authed({
      token: reporter,
      method: "POST",
      path: "/incidents",
      body: { title: "ws two", severity: "P2" },
      expectedStatus: 201
    });

    const replayMissed = await new Promise<Array<{ eventId: number; type: string }>>((resolve, reject) => {
      const socket = new WebSocket(
        `${server.url.replace("http", "ws")}/ws?lastEventId=${lastSeen}`
      );
      const events: Array<{ eventId: number; type: string }> = [];

      const timeout = setTimeout(() => {
        socket.close();
        reject(new Error("timeout while waiting for missed replay"));
      }, 4000);

      socket.on("message", payload => {
        events.push(JSON.parse(payload.toString()) as { eventId: number; type: string });
        clearTimeout(timeout);
        socket.close();
        resolve(events);
      });

      socket.on("error", error => {
        clearTimeout(timeout);
        reject(error);
      });
    });

    expect(replayMissed.length).toBeGreaterThanOrEqual(1);
    expect(replayMissed[0]?.eventId).toBeGreaterThan(lastSeen);
    expect(replayMissed[0]?.type).toBe("incident.created");
  });
});
