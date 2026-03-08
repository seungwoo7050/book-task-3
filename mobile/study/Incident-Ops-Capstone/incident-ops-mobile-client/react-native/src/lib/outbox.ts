import type { Incident, QueueAction } from '../contracts';
import type { IncidentListItem, QueuedMutation } from './types';
import { MAX_OUTBOX_ATTEMPTS } from './types';

function safeString(value: unknown): string {
  return typeof value === 'string' ? value : '';
}

export function createQueuedMutation(input: {
  action: QueueAction;
  payload: Record<string, unknown>;
  label: string;
  createdAt: string;
  idGenerator: () => string;
}): QueuedMutation {
  return {
    id: input.idGenerator(),
    action: input.action,
    payload: input.payload,
    idempotencyKey: input.idGenerator(),
    attempts: 0,
    state: 'pending',
    lastError: null,
    label: input.label,
    createdAt: input.createdAt,
  };
}

export function markQueuedMutationSynced(item: QueuedMutation): QueuedMutation {
  return {
    ...item,
    attempts: item.attempts + 1,
    state: 'synced',
    lastError: null,
  };
}

export function markQueuedMutationFailed(
  item: QueuedMutation,
  error: unknown,
): QueuedMutation {
  const attempts = item.attempts + 1;
  const lastError = error instanceof Error ? error.message : 'unknown error';

  return {
    ...item,
    attempts,
    state: attempts >= MAX_OUTBOX_ATTEMPTS ? 'failed' : 'pending',
    lastError,
  };
}

export function retryQueuedMutation(item: QueuedMutation): QueuedMutation {
  return {
    ...item,
    state: 'pending',
    lastError: null,
  };
}

export function summarizeOutbox(outbox: QueuedMutation[]) {
  return {
    pending: outbox.filter(item => item.state === 'pending').length,
    synced: outbox.filter(item => item.state === 'synced').length,
    failed: outbox.filter(item => item.state === 'failed').length,
  };
}

function applyActionToIncident(
  incident: Incident,
  item: QueuedMutation,
): Incident {
  const incidentId = safeString(item.payload.incidentId);

  if (!incidentId || incidentId !== incident.id) {
    return incident;
  }

  switch (item.action) {
    case 'POST /incidents/:id/ack':
      return {
        ...incident,
        status: 'ACKED',
      };
    case 'POST /incidents/:id/request-resolution':
      return {
        ...incident,
        status: 'RESOLUTION_PENDING',
      };
    case 'POST /approvals/:id/decision':
      return {
        ...incident,
        status:
          safeString(item.payload.decision) === 'APPROVE' ? 'RESOLVED' : 'ACKED',
      };
    default:
      return incident;
  }
}

function toOptimisticIncident(item: QueuedMutation): IncidentListItem | null {
  if (item.action !== 'POST /incidents' || item.state === 'synced') {
    return null;
  }

  return {
    id: `local-${item.id}`,
    title: safeString(item.payload.title) || 'Queued incident',
    description: safeString(item.payload.description),
    severity:
      safeString(item.payload.severity) === 'P1' ||
      safeString(item.payload.severity) === 'P2'
        ? (item.payload.severity as Incident['severity'])
        : 'P3',
    status: 'OPEN',
    createdBy: 'local-user',
    approvalId: null,
    createdAt: item.createdAt,
    updatedAt: item.createdAt,
    source: 'optimistic',
    syncState: item.state === 'failed' ? 'failed' : 'queued',
    pendingActions: [item.action],
  };
}

export function buildIncidentList(
  serverIncidents: Incident[],
  outbox: QueuedMutation[],
): IncidentListItem[] {
  const optimisticItems = outbox
    .map(toOptimisticIncident)
    .filter((item): item is IncidentListItem => item !== null);

  const serverItems = serverIncidents.map(incident => {
    const related = outbox.filter(item => {
      if (item.action === 'POST /incidents') {
        return false;
      }

      return safeString(item.payload.incidentId) === incident.id;
    });

    let nextIncident = incident;
    for (const item of related) {
      if (item.state === 'synced') {
        continue;
      }

      nextIncident = applyActionToIncident(nextIncident, item);
    }

    return {
      ...nextIncident,
      source: 'server' as const,
      syncState: related.some(item => item.state === 'failed')
        ? ('failed' as const)
        : related.some(item => item.state === 'pending')
          ? ('queued' as const)
          : ('live' as const),
      pendingActions: related
        .filter(item => item.state !== 'synced')
        .map(item => item.action),
    };
  });

  return [...optimisticItems, ...serverItems];
}
