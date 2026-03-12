import { randomUUID } from "node:crypto";
import {
  type QueueAction,
  type QueueJob,
} from "../../../problem/code/contracts/contracts";

interface QueueExecutor {
  (job: QueueJob): Promise<void>;
}

export class OfflineQueueEngine {
  private readonly jobs = new Map<string, QueueJob>();
  private readonly maxAttempts: number;

  constructor(maxAttempts = 3) {
    this.maxAttempts = maxAttempts;
  }

  enqueue(action: QueueAction, payload: Record<string, unknown>): QueueJob {
    const job: QueueJob = {
      id: randomUUID(),
      action,
      payload,
      idempotencyKey: randomUUID(),
      attempts: 0,
      state: "pending",
      lastError: null
    };

    this.jobs.set(job.id, job);
    return job;
  }

  list(): QueueJob[] {
    return [...this.jobs.values()];
  }

  summary(): { pending: number; synced: number; failed: number } {
    const values = this.list();
    return {
      pending: values.filter(item => item.state === "pending").length,
      synced: values.filter(item => item.state === "synced").length,
      failed: values.filter(item => item.state === "failed").length
    };
  }

  async flush(executor: QueueExecutor): Promise<void> {
    for (const job of this.list()) {
      if (job.state !== "pending") {
        continue;
      }

      try {
        await executor(job);
        this.jobs.set(job.id, {
          ...job,
          attempts: job.attempts + 1,
          state: "synced",
          lastError: null
        });
      } catch (error) {
        const attempts = job.attempts + 1;
        this.jobs.set(job.id, {
          ...job,
          attempts,
          state: attempts >= this.maxAttempts ? "failed" : "pending",
          lastError: error instanceof Error ? error.message : "unknown error"
        });
      }
    }
  }
}
