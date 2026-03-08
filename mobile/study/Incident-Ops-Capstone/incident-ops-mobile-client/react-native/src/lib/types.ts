import type { AuthActor, Incident, QueueAction, QueueJob } from '../contracts';

export const DEFAULT_BASE_URL = 'http://127.0.0.1:4100';
export const MAX_OUTBOX_ATTEMPTS = 3;

export interface AppSettings {
  baseUrl: string;
}

export interface AppSession {
  token: string;
  actor: AuthActor;
}

export interface ConnectionState {
  isConnected: boolean;
  typeLabel: string;
  updatedAt: string;
}

export type StreamStatus = 'idle' | 'connecting' | 'live' | 'error';

export interface QueuedMutation extends QueueJob {
  label: string;
  createdAt: string;
}

export interface IncidentListItem extends Incident {
  source: 'server' | 'optimistic';
  syncState: 'live' | 'queued' | 'failed';
  pendingActions: QueueAction[];
}
