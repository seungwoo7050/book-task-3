import {
  applyReplayEvents,
  createPendingMessage,
  dedupeReplay,
  reconcileAck,
  updateTypingState,
} from '../src/chatModel';

describe('realtime chat model', () => {
  it('reconciles an ack into a pending message', () => {
    const pending = createPendingMessage('general', 'client-1', 'hello');
    expect(
      reconcileAck([pending], { clientId: 'client-1', serverId: 'srv-1' })[0],
    ).toMatchObject({
      serverId: 'srv-1',
      status: 'sent',
    });
  });

  it('filters replay events by lastEventId', () => {
    expect(
      applyReplayEvents(
        [
          { eventId: 1, serverId: 'srv-1', text: 'old' },
          { eventId: 2, serverId: 'srv-2', text: 'new' },
        ],
        1,
      ),
    ).toEqual([{ eventId: 2, serverId: 'srv-2', text: 'new' }]);
  });

  it('dedupes replay by server id and tracks typing state', () => {
    expect(
      dedupeReplay([
        { eventId: 2, serverId: 'srv-2', text: 'a' },
        { eventId: 3, serverId: 'srv-2', text: 'duplicate' },
      ]),
    ).toHaveLength(1);
    expect(updateTypingState({}, 'alice', true)).toEqual({ alice: true });
  });
});
