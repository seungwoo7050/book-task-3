import type { StreamEvent } from '../contracts';
import { buildWebsocketUrl } from './api';

interface OpenStreamInput {
  baseUrl: string;
  lastEventId: number;
  onEvent: (event: StreamEvent) => void;
  onOpen?: () => void;
  onClose?: () => void;
  onError?: () => void;
}

export function openIncidentStream(input: OpenStreamInput): () => void {
  const socket = new WebSocket(
    buildWebsocketUrl(input.baseUrl, input.lastEventId),
  );

  socket.onopen = () => {
    input.onOpen?.();
  };

  socket.onerror = () => {
    input.onError?.();
  };

  socket.onclose = () => {
    input.onClose?.();
  };

  socket.onmessage = event => {
    const parsed = JSON.parse(event.data) as StreamEvent;
    input.onEvent(parsed);
  };

  return () => {
    socket.close();
  };
}
