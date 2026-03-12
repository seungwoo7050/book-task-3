import type {
  Approval,
  ApprovalDecision,
  AuditLog,
  AuthActor,
  Incident,
  StreamEvent,
  UserRole,
} from './contracts';

export const initialIncident: Incident = {
  id: 'inc-1',
  title: 'Database latency spike',
  description: 'Checkout queries exceed SLO for 10 minutes',
  severity: 'P1',
  status: 'OPEN',
  createdBy: 'reporter.demo',
  approvalId: null,
  createdAt: '2026-03-08T09:00:00.000Z',
  updatedAt: '2026-03-08T09:00:00.000Z',
};

export const initialApproval: Approval = {
  id: 'apr-1',
  incidentId: 'inc-1',
  requestedBy: 'operator.demo',
  status: 'PENDING',
  decision: null,
  note: null,
  decidedBy: null,
  decidedAt: null,
  createdAt: '2026-03-08T09:10:00.000Z',
  updatedAt: '2026-03-08T09:10:00.000Z',
};

export const initialAuditLogs: AuditLog[] = [
  {
    id: 1,
    incidentId: 'inc-1',
    actorId: 'reporter.demo',
    actorRole: 'REPORTER',
    action: 'incident.created',
    result: 'SUCCESS',
    detail: 'Initial incident opened from mobile harness',
    createdAt: '2026-03-08T09:00:00.000Z',
  },
];

export const streamEvents: StreamEvent[] = [
  {
    eventId: 1,
    type: 'incident.created',
    timestamp: '2026-03-08T09:00:00.000Z',
    payload: { incidentId: 'inc-1' },
  },
  {
    eventId: 2,
    type: 'incident.updated',
    timestamp: '2026-03-08T09:04:00.000Z',
    payload: { incidentId: 'inc-1', status: 'ACKED' },
  },
  {
    eventId: 3,
    type: 'approval.requested',
    timestamp: '2026-03-08T09:10:00.000Z',
    payload: { approvalId: 'apr-1', incidentId: 'inc-1' },
  },
  {
    eventId: 4,
    type: 'approval.decided',
    timestamp: '2026-03-08T09:20:00.000Z',
    payload: { approvalId: 'apr-1', decision: 'APPROVE' },
  },
];

export function loginAs(role: UserRole): AuthActor {
  return {
    userId: `${role.toLowerCase()}.demo`,
    role,
  };
}

export function listAvailableActions(
  actor: AuthActor,
  incident: Incident,
  approval: Approval | null,
): string[] {
  if (actor.role === 'OPERATOR' && incident.status === 'OPEN') {
    return ['ack'];
  }

  if (actor.role === 'OPERATOR' && incident.status === 'ACKED') {
    return ['request-resolution'];
  }

  if (actor.role === 'APPROVER' && approval?.status === 'PENDING') {
    return ['approve', 'reject'];
  }

  return [];
}

export function acknowledgeIncident(
  incident: Incident,
  actor: AuthActor,
): { incident: Incident; auditLog: AuditLog } {
  return {
    incident: {
      ...incident,
      status: 'ACKED',
      updatedAt: '2026-03-08T09:04:00.000Z',
    },
    auditLog: {
      id: 2,
      incidentId: incident.id,
      actorId: actor.userId,
      actorRole: actor.role,
      action: 'incident.ack',
      result: 'SUCCESS',
      detail: 'Operator acknowledged the incident',
      createdAt: '2026-03-08T09:04:00.000Z',
    },
  };
}

export function requestResolution(
  incident: Incident,
  actor: AuthActor,
): { incident: Incident; approval: Approval; auditLog: AuditLog } {
  const approval: Approval = {
    ...initialApproval,
    requestedBy: actor.userId,
  };

  return {
    incident: {
      ...incident,
      status: 'RESOLUTION_PENDING',
      approvalId: approval.id,
      updatedAt: '2026-03-08T09:10:00.000Z',
    },
    approval,
    auditLog: {
      id: 3,
      incidentId: incident.id,
      actorId: actor.userId,
      actorRole: actor.role,
      action: 'approval.requested',
      result: 'SUCCESS',
      detail: 'Resolution request submitted for approval',
      createdAt: '2026-03-08T09:10:00.000Z',
    },
  };
}

export function decideApproval(
  incident: Incident,
  approval: Approval,
  actor: AuthActor,
  decision: ApprovalDecision,
): { incident: Incident; approval: Approval; auditLog: AuditLog } {
  const nextApproval: Approval = {
    ...approval,
    status: decision === 'APPROVE' ? 'APPROVED' : 'REJECTED',
    decision,
    decidedBy: actor.userId,
    decidedAt: '2026-03-08T09:20:00.000Z',
    updatedAt: '2026-03-08T09:20:00.000Z',
  };

  return {
    incident: {
      ...incident,
      status: decision === 'APPROVE' ? 'RESOLVED' : 'ACKED',
      updatedAt: '2026-03-08T09:20:00.000Z',
    },
    approval: nextApproval,
    auditLog: {
      id: 4,
      incidentId: incident.id,
      actorId: actor.userId,
      actorRole: actor.role,
      action: 'approval.decided',
      result: 'SUCCESS',
      detail: `Approver selected ${decision}`,
      createdAt: '2026-03-08T09:20:00.000Z',
    },
  };
}

export function replayFrom(lastEventId: number): StreamEvent[] {
  return streamEvents.filter(event => event.eventId > lastEventId);
}
