import { createMemoryStorage, loadLastEventId, loadOutbox, loadSession, loadSettings, saveLastEventId, saveOutbox, saveSession, saveSettings } from '../src/lib/storage';

describe('storage helpers', () => {
  it('round-trips session, settings, outbox, and event cursor', async () => {
    const storage = createMemoryStorage();

    await saveSettings({ baseUrl: 'http://localhost:4100' }, storage);
    await saveSession(
      {
        token: 'token-1',
        actor: {
          userId: 'reporter.demo',
          role: 'REPORTER',
        },
      },
      storage,
    );
    await saveOutbox(
      [
        {
          id: 'job-1',
          action: 'POST /incidents',
          payload: { title: 'offline' },
          idempotencyKey: 'idem-1',
          attempts: 1,
          state: 'pending',
          lastError: null,
          label: 'Create offline',
          createdAt: '2026-03-07T00:00:00.000Z',
        },
      ],
      storage,
    );
    await saveLastEventId(12, storage);

    await expect(loadSettings(storage)).resolves.toEqual({
      baseUrl: 'http://localhost:4100',
    });
    await expect(loadSession(storage)).resolves.toMatchObject({
      token: 'token-1',
      actor: {
        userId: 'reporter.demo',
      },
    });
    await expect(loadOutbox(storage)).resolves.toHaveLength(1);
    await expect(loadLastEventId(storage)).resolves.toBe(12);
  });
});
