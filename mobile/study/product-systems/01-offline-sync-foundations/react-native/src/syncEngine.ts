export type QueueState = 'pending' | 'synced' | 'failed' | 'dlq';

export interface TaskRecord {
  localId: string;
  serverId: string | null;
  title: string;
  status: 'draft' | 'synced';
  updatedAt: string;
}

export interface QueueJob {
  id: string;
  action: 'create-task';
  taskLocalId: string;
  payload: Pick<TaskRecord, 'title'>;
  idempotencyKey: string;
  attempts: number;
  state: QueueState;
  lastError: string | null;
}

export function createTaskDraft(title: string, sequence: number): {
  task: TaskRecord;
  job: QueueJob;
} {
  const localId = `local-${sequence}`;
  const idempotencyKey = `create-${localId}`;

  return {
    task: {
      localId,
      serverId: null,
      title,
      status: 'draft',
      updatedAt: `2026-03-08T00:00:${String(sequence).padStart(2, '0')}Z`,
    },
    job: {
      id: `job-${sequence}`,
      action: 'create-task',
      taskLocalId: localId,
      payload: { title },
      idempotencyKey,
      attempts: 0,
      state: 'pending',
      lastError: null,
    },
  };
}

export class FakeSyncServer {
  private seenKeys = new Map<string, string>();

  syncCreate(job: QueueJob): { serverId: string; accepted: boolean } {
    if (job.payload.title.includes('FAIL')) {
      throw new Error('server rejected payload');
    }

    const existing = this.seenKeys.get(job.idempotencyKey);
    if (existing) {
      return { serverId: existing, accepted: false };
    }

    const serverId = `srv-${this.seenKeys.size + 1}`;
    this.seenKeys.set(job.idempotencyKey, serverId);
    return { serverId, accepted: true };
  }
}

export function mergeServerAssignedFields(
  server: { serverId: string; updatedAt?: string },
  client: TaskRecord,
): TaskRecord {
  return {
    ...client,
    serverId: server.serverId,
    updatedAt: server.updatedAt ?? client.updatedAt,
    status: 'synced',
  };
}

export function flushQueue(
  tasks: TaskRecord[],
  jobs: QueueJob[],
  server: FakeSyncServer,
  maxAttempts = 2,
): { tasks: TaskRecord[]; jobs: QueueJob[] } {
  const nextTasks = [...tasks];
  const nextJobs = jobs.map(job => ({ ...job }));

  nextJobs.forEach(job => {
    if (job.state !== 'pending' && job.state !== 'failed') {
      return;
    }

    try {
      const response = server.syncCreate(job);
      const taskIndex = nextTasks.findIndex(task => task.localId === job.taskLocalId);
      if (taskIndex >= 0) {
        nextTasks[taskIndex] = mergeServerAssignedFields(
          {
            serverId: response.serverId,
            updatedAt: `2026-03-08T01:00:0${taskIndex}Z`,
          },
          nextTasks[taskIndex],
        );
      }
      job.state = 'synced';
      job.lastError = null;
    } catch (error) {
      job.attempts += 1;
      job.lastError = error instanceof Error ? error.message : 'unknown';
      job.state = job.attempts >= maxAttempts ? 'dlq' : 'failed';
    }
  });

  return { tasks: nextTasks, jobs: nextJobs };
}
