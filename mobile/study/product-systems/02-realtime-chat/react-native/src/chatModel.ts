export interface MessageRecord {
  clientId: string;
  serverId: string | null;
  conversationId: string;
  text: string;
  status: 'pending' | 'sent';
}

export interface ReplayEvent {
  eventId: number;
  serverId: string;
  text: string;
}

export function createPendingMessage(
  conversationId: string,
  clientId: string,
  text: string,
): MessageRecord {
  return {
    clientId,
    serverId: null,
    conversationId,
    text,
    status: 'pending',
  };
}

export function reconcileAck(
  messages: MessageRecord[],
  ack: { clientId: string; serverId: string },
): MessageRecord[] {
  return messages.map(message =>
    message.clientId === ack.clientId
      ? { ...message, serverId: ack.serverId, status: 'sent' }
      : message,
  );
}

export function applyReplayEvents(events: ReplayEvent[], lastEventId: number): ReplayEvent[] {
  return events.filter(event => event.eventId > lastEventId);
}

export function dedupeReplay(events: ReplayEvent[]): ReplayEvent[] {
  const seen = new Set<string>();
  return events.filter(event => {
    if (seen.has(event.serverId)) {
      return false;
    }

    seen.add(event.serverId);
    return true;
  });
}

export function updateTypingState(
  state: Record<string, boolean>,
  userId: string,
  isTyping: boolean,
): Record<string, boolean> {
  return {
    ...state,
    [userId]: isTyping,
  };
}
