import {
  FakeSyncServer,
  createTaskDraft,
  flushQueue,
  mergeServerAssignedFields,
} from '../src/syncEngine';

describe('offline sync engine', () => {
  it('syncs a pending task and assigns server id', () => {
    const created = createTaskDraft('Investigate queue', 1);
    const result = flushQueue([created.task], [created.job], new FakeSyncServer());
    expect(result.tasks[0].serverId).toBe('srv-1');
    expect(result.jobs[0].state).toBe('synced');
  });

  it('moves a repeatedly failing job to dlq', () => {
    const created = createTaskDraft('FAIL replay', 2);
    const once = flushQueue([created.task], [created.job], new FakeSyncServer());
    const twice = flushQueue(once.tasks, once.jobs, new FakeSyncServer());
    expect(twice.jobs[0].state).toBe('dlq');
  });

  it('keeps idempotency stable on duplicate flushes', () => {
    const created = createTaskDraft('Keep key stable', 3);
    const server = new FakeSyncServer();
    const once = flushQueue([created.task], [created.job], server);
    const twice = flushQueue(once.tasks, once.jobs, server);
    expect(twice.tasks[0].serverId).toBe('srv-1');
  });

  it('merges server-assigned fields while preserving title', () => {
    const created = createTaskDraft('Merge me', 4);
    expect(
      mergeServerAssignedFields(
        { serverId: 'srv-99', updatedAt: '2026-03-08T01:00:00Z' },
        created.task,
      ),
    ).toMatchObject({
      serverId: 'srv-99',
      title: 'Merge me',
      status: 'synced',
    });
  });
});
