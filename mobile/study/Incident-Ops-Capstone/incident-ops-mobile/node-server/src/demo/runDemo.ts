import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { WebSocket } from "ws";
import { startIncidentOpsServer } from "../server";
import { OfflineQueueEngine } from "./offlineQueue";
import {
  type QueueJob,
  type StreamEvent,
} from "../../../problem/code/contracts/contracts";

function assertOk(response: Response, context: string): void {
  if (!response.ok) {
    throw new Error(`${context} failed: ${response.status}`);
  }
}

async function login(baseUrl: string, userId: string, role: "REPORTER" | "OPERATOR" | "APPROVER"): Promise<string> {
  const response = await fetch(`${baseUrl}/auth/login`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ userId, role })
  });
  assertOk(response, "login");
  const body = (await response.json()) as { token: string };
  return body.token;
}

async function authedJson<T>(input: {
  baseUrl: string;
  token: string;
  method: "GET" | "POST";
  path: string;
  idempotencyKey?: string;
  body?: unknown;
}): Promise<T> {
  const response = await fetch(`${input.baseUrl}${input.path}`, {
    method: input.method,
    headers: {
      authorization: `Bearer ${input.token}`,
      "content-type": "application/json",
      ...(input.idempotencyKey ? { "x-idempotency-key": input.idempotencyKey } : {})
    },
    body: input.body ? JSON.stringify(input.body) : undefined
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`${input.method} ${input.path} failed (${response.status}) ${text}`);
  }

  return (await response.json()) as T;
}

async function main(): Promise<void> {
  const server = await startIncidentOpsServer();
  const logLines: string[] = [];

  try {
    const reporterToken = await login(server.url, "reporter.demo", "REPORTER");
    const operatorToken = await login(server.url, "operator.demo", "OPERATOR");
    const approverToken = await login(server.url, "approver.demo", "APPROVER");

    logLines.push("[step] authenticated reporter/operator/approver");

    const queue = new OfflineQueueEngine(3);
    const queuedCreate = queue.enqueue("POST /incidents", {
      title: "Offline queue incident",
      description: "created while app offline",
      severity: "P2"
    });

    let online = false;
    const executeQueueJob = async (job: QueueJob): Promise<void> => {
      if (!online) {
        throw new Error("NETWORK_UNAVAILABLE");
      }

      if (job.action === "POST /incidents") {
        await authedJson({
          baseUrl: server.url,
          token: reporterToken,
          method: "POST",
          path: "/incidents",
          idempotencyKey: job.idempotencyKey,
          body: job.payload
        });
      }
    };

    await queue.flush(executeQueueJob);
    logLines.push(`[step] offline flush summary ${JSON.stringify(queue.summary())}`);

    online = true;
    await queue.flush(executeQueueJob);
    logLines.push(`[step] recovery flush summary ${JSON.stringify(queue.summary())}`);

    const listAfterSync = await authedJson<{
      incidents: Array<{ id: string; status: string }>;
    }>({
      baseUrl: server.url,
      token: operatorToken,
      method: "GET",
      path: "/incidents?limit=10"
    });

    const primaryIncidentId = listAfterSync.incidents[0]?.id;
    if (!primaryIncidentId) {
      throw new Error("missing primary incident after offline recovery");
    }

    const ackResult = await authedJson<{ incident: { id: string; status: string } }>({
      baseUrl: server.url,
      token: operatorToken,
      method: "POST",
      path: `/incidents/${primaryIncidentId}/ack`,
      idempotencyKey: "demo-ack-primary"
    });

    const resolutionResult = await authedJson<{
      incident: { id: string; status: string };
      approval: { id: string; status: string };
    }>({
      baseUrl: server.url,
      token: operatorToken,
      method: "POST",
      path: `/incidents/${primaryIncidentId}/request-resolution`,
      idempotencyKey: "demo-resolution-primary",
      body: { reason: "incident mitigated" }
    });

    const approveResult = await authedJson<{
      incident: { id: string; status: string };
      approval: { id: string; status: string };
    }>({
      baseUrl: server.url,
      token: approverToken,
      method: "POST",
      path: `/approvals/${resolutionResult.approval.id}/decision`,
      idempotencyKey: "demo-approve-primary",
      body: { decision: "APPROVE", note: "validated and closed" }
    });

    logLines.push(
      `[step] approval approved incident=${approveResult.incident.id} status=${approveResult.incident.status}`
    );

    const secondCreate = await authedJson<{ incident: { id: string } }>({
      baseUrl: server.url,
      token: reporterToken,
      method: "POST",
      path: "/incidents",
      idempotencyKey: "demo-create-second",
      body: {
        title: "Reject branch incident",
        description: "used for reject safe stop",
        severity: "P3"
      }
    });

    await authedJson({
      baseUrl: server.url,
      token: operatorToken,
      method: "POST",
      path: `/incidents/${secondCreate.incident.id}/ack`,
      idempotencyKey: "demo-ack-second"
    });

    const secondResolution = await authedJson<{
      approval: { id: string };
    }>({
      baseUrl: server.url,
      token: operatorToken,
      method: "POST",
      path: `/incidents/${secondCreate.incident.id}/request-resolution`,
      idempotencyKey: "demo-resolution-second",
      body: { reason: "operator requested close" }
    });

    const rejectResult = await authedJson<{ incident: { status: string } }>({
      baseUrl: server.url,
      token: approverToken,
      method: "POST",
      path: `/approvals/${secondResolution.approval.id}/decision`,
      idempotencyKey: "demo-reject-second",
      body: { decision: "REJECT", note: "need more evidence" }
    });

    logLines.push(`[step] approval rejected status=${rejectResult.incident.status}`);

    const dlqQueue = new OfflineQueueEngine(3);
    dlqQueue.enqueue("POST /incidents/:id/ack", {
      incidentId: secondCreate.incident.id
    });

    const failingExecutor = async (_job: QueueJob): Promise<void> => {
      throw new Error("SERVER_5XX");
    };

    await dlqQueue.flush(failingExecutor);
    await dlqQueue.flush(failingExecutor);
    await dlqQueue.flush(failingExecutor);

    logLines.push(`[step] dlq summary ${JSON.stringify(dlqQueue.summary())}`);

    const wsFirstEvents: StreamEvent[] = await new Promise((resolve, reject) => {
      const socket = new WebSocket(`${server.url.replace("http", "ws")}/ws?lastEventId=0`);
      const events: StreamEvent[] = [];

      const timeout = setTimeout(() => {
        socket.close();
        reject(new Error("ws initial timeout"));
      }, 4000);

      socket.on("message", payload => {
        events.push(JSON.parse(payload.toString()) as StreamEvent);
        if (events.length >= 2) {
          clearTimeout(timeout);
          socket.close();
          resolve(events);
        }
      });

      socket.on("error", error => {
        clearTimeout(timeout);
        reject(error);
      });
    });

    const lastEventId = wsFirstEvents[wsFirstEvents.length - 1]?.eventId ?? 0;

    await authedJson({
      baseUrl: server.url,
      token: reporterToken,
      method: "POST",
      path: "/incidents",
      idempotencyKey: "demo-ws-replay-create",
      body: {
        title: "Replay verification incident",
        description: "created while subscriber disconnected",
        severity: "P1"
      }
    });

    const replayedEvents: StreamEvent[] = await new Promise((resolve, reject) => {
      const socket = new WebSocket(
        `${server.url.replace("http", "ws")}/ws?lastEventId=${lastEventId}`
      );
      const events: StreamEvent[] = [];

      const timeout = setTimeout(() => {
        socket.close();
        reject(new Error("ws replay timeout"));
      }, 4000);

      socket.on("message", payload => {
        events.push(JSON.parse(payload.toString()) as StreamEvent);
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
    });

    logLines.push(`[step] ws replay events=${replayedEvents.length}`);

    const audit = await authedJson<{ items: unknown[] }>({
      baseUrl: server.url,
      token: approverToken,
      method: "GET",
      path: `/audit?incidentId=${primaryIncidentId}`
    });

    const summary = {
      incidentFlow: {
        queuedCreateJobId: queuedCreate.id,
        ackStatus: ackResult.incident.status,
        approvedStatus: approveResult.incident.status,
        rejectedStatus: rejectResult.incident.status
      },
      recovery: {
        offlineQueue: queue.summary(),
        dlqQueue: dlqQueue.summary()
      },
      websocket: {
        initialEvents: wsFirstEvents.length,
        replayedEvents: replayedEvents.length,
        replayFromEventId: lastEventId
      },
      auditRecords: audit.items.length,
      structuredLogCount: server.structuredLogs.length
    };

    const outputDir = resolve(__dirname, "../../../demo");
    mkdirSync(outputDir, { recursive: true });

    const summaryPath = resolve(outputDir, "e2e-summary.json");
    const logPath = resolve(outputDir, "e2e-run.log");
    const auditPath = resolve(outputDir, "audit-log.json");
    const structuredPath = resolve(outputDir, "structured-logs.json");

    writeFileSync(summaryPath, `${JSON.stringify(summary, null, 2)}\n`, "utf8");
    writeFileSync(logPath, `${logLines.join("\n")}\n`, "utf8");
    writeFileSync(auditPath, `${JSON.stringify(audit, null, 2)}\n`, "utf8");
    writeFileSync(structuredPath, `${JSON.stringify(server.structuredLogs, null, 2)}\n`, "utf8");

    // Keep a stable stdout marker for make target logs.
    process.stdout.write(`demo artifacts written to ${dirname(summaryPath)}\n`);
  } finally {
    await server.stop();
  }
}

void main();
