import { buildIncidentList, createQueuedMutation, markQueuedMutationFailed, retryQueuedMutation } from '../src/lib/outbox';
import type { Incident } from '../src/contracts';

describe('outbox helpers', () => {
  it('moves a job into failed after max attempts', () => {
    const base = createQueuedMutation({
      action: 'POST /incidents/:id/ack',
      payload: { incidentId: 'inc-1' },
      label: 'Ack inc-1',
      createdAt: '2026-03-07T00:00:00.000Z',
      idGenerator: () => 'job-fixed',
    });

    const first = markQueuedMutationFailed(base, new Error('offline'));
    const second = markQueuedMutationFailed(first, new Error('still offline'));
    const third = markQueuedMutationFailed(second, new Error('server 503'));

    expect(first.state).toBe('pending');
    expect(second.state).toBe('pending');
    expect(third.state).toBe('failed');
    expect(third.attempts).toBe(3);
  });

  it('applies optimistic state to an incident list', () => {
    const incident: Incident = {
      id: 'inc-1',
      title: 'Primary incident',
      description: 'server copy',
      severity: 'P1',
      status: 'OPEN',
      createdBy: 'reporter.demo',
      approvalId: null,
      createdAt: '2026-03-07T00:00:00.000Z',
      updatedAt: '2026-03-07T00:00:00.000Z',
    };

    const queuedCreate = createQueuedMutation({
      action: 'POST /incidents',
      payload: {
        title: 'Offline incident',
        description: 'queued while offline',
        severity: 'P2',
      },
      label: 'Create Offline incident',
      createdAt: '2026-03-07T00:01:00.000Z',
      idGenerator: () => 'job-create',
    });

    const queuedAck = createQueuedMutation({
      action: 'POST /incidents/:id/ack',
      payload: { incidentId: 'inc-1' },
      label: 'Ack inc-1',
      createdAt: '2026-03-07T00:02:00.000Z',
      idGenerator: () => 'job-ack',
    });

    const items = buildIncidentList([incident], [queuedCreate, queuedAck]);

    expect(items[0]?.source).toBe('optimistic');
    expect(items[0]?.title).toBe('Offline incident');
    expect(items[1]?.id).toBe('inc-1');
    expect(items[1]?.status).toBe('ACKED');
    expect(items[1]?.syncState).toBe('queued');
  });

  it('resets a failed job back to pending for manual retry', () => {
    const failed = {
      ...createQueuedMutation({
        action: 'POST /incidents',
        payload: { title: 'retry me', severity: 'P3' },
        label: 'Create retry me',
        createdAt: '2026-03-07T00:00:00.000Z',
        idGenerator: () => 'job-retry',
      }),
      state: 'failed' as const,
      lastError: '503',
      attempts: 3,
    };

    const retried = retryQueuedMutation(failed);
    expect(retried.state).toBe('pending');
    expect(retried.lastError).toBeNull();
    expect(retried.attempts).toBe(3);
  });
});
