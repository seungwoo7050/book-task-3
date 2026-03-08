import type {
  Approval,
  ApprovalDecision,
  AuditLog,
  CreateIncidentRequest,
  Incident,
  LoginResponse,
  RequestResolutionBody,
} from '../contracts';

export interface IncidentPageResponse {
  incidents: Incident[];
  nextCursor: string | null;
}

export interface IncidentMutationResponse {
  incident: Incident;
  approval?: Approval;
  eventId: number;
}

export interface AuditResponse {
  items: AuditLog[];
}

interface RequestJsonInput {
  baseUrl: string;
  path: string;
  method: 'GET' | 'POST';
  token?: string;
  body?: unknown;
  idempotencyKey?: string;
}

export class ApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

export function normalizeBaseUrl(value: string): string {
  return value.trim().replace(/\/+$/, '');
}

export function buildWebsocketUrl(baseUrl: string, lastEventId: number): string {
  const normalized = normalizeBaseUrl(baseUrl);
  const url = new URL(`${normalized}/ws`);
  url.protocol = url.protocol === 'https:' ? 'wss:' : 'ws:';
  url.searchParams.set('lastEventId', String(lastEventId));
  return url.toString();
}

async function requestJson<T>(input: RequestJsonInput): Promise<T> {
  const response = await fetch(`${normalizeBaseUrl(input.baseUrl)}${input.path}`, {
    method: input.method,
    headers: {
      'content-type': 'application/json',
      ...(input.token ? { authorization: `Bearer ${input.token}` } : {}),
      ...(input.idempotencyKey
        ? { 'x-idempotency-key': input.idempotencyKey }
        : {}),
    },
    body: input.body ? JSON.stringify(input.body) : undefined,
  });

  const text = await response.text();
  const body = text ? (JSON.parse(text) as Record<string, unknown>) : null;

  if (!response.ok) {
    throw new ApiError(
      response.status,
      typeof body?.error === 'string'
        ? body.error
        : `${input.method} ${input.path} failed`,
    );
  }

  return body as T;
}

export function loginRequest(input: {
  baseUrl: string;
  userId: string;
  role: 'REPORTER' | 'OPERATOR' | 'APPROVER';
}): Promise<LoginResponse> {
  return requestJson<LoginResponse>({
    baseUrl: input.baseUrl,
    path: '/auth/login',
    method: 'POST',
    body: {
      userId: input.userId,
      role: input.role,
    },
  });
}

export function listIncidents(input: {
  baseUrl: string;
  token: string;
  cursor: string | null;
  limit?: number;
}): Promise<IncidentPageResponse> {
  const query = new URLSearchParams();
  query.set('limit', String(input.limit ?? 12));
  if (input.cursor) {
    query.set('cursor', input.cursor);
  }

  return requestJson<IncidentPageResponse>({
    baseUrl: input.baseUrl,
    path: `/incidents?${query.toString()}`,
    method: 'GET',
    token: input.token,
  });
}

export function listAudit(input: {
  baseUrl: string;
  token: string;
  incidentId: string;
}): Promise<AuditResponse> {
  return requestJson<AuditResponse>({
    baseUrl: input.baseUrl,
    path: `/audit?incidentId=${input.incidentId}`,
    method: 'GET',
    token: input.token,
  });
}

export function createIncidentRequest(input: {
  baseUrl: string;
  token: string;
  idempotencyKey: string;
  body: CreateIncidentRequest;
}): Promise<IncidentMutationResponse> {
  return requestJson<IncidentMutationResponse>({
    baseUrl: input.baseUrl,
    path: '/incidents',
    method: 'POST',
    token: input.token,
    idempotencyKey: input.idempotencyKey,
    body: input.body,
  });
}

export function acknowledgeIncidentRequest(input: {
  baseUrl: string;
  token: string;
  idempotencyKey: string;
  incidentId: string;
}): Promise<IncidentMutationResponse> {
  return requestJson<IncidentMutationResponse>({
    baseUrl: input.baseUrl,
    path: `/incidents/${input.incidentId}/ack`,
    method: 'POST',
    token: input.token,
    idempotencyKey: input.idempotencyKey,
  });
}

export function requestResolutionRequest(input: {
  baseUrl: string;
  token: string;
  idempotencyKey: string;
  incidentId: string;
  body: RequestResolutionBody;
}): Promise<IncidentMutationResponse> {
  return requestJson<IncidentMutationResponse>({
    baseUrl: input.baseUrl,
    path: `/incidents/${input.incidentId}/request-resolution`,
    method: 'POST',
    token: input.token,
    idempotencyKey: input.idempotencyKey,
    body: input.body,
  });
}

export function decideApprovalRequest(input: {
  baseUrl: string;
  token: string;
  idempotencyKey: string;
  approvalId: string;
  decision: ApprovalDecision;
  note?: string;
}): Promise<IncidentMutationResponse> {
  return requestJson<IncidentMutationResponse>({
    baseUrl: input.baseUrl,
    path: `/approvals/${input.approvalId}/decision`,
    method: 'POST',
    token: input.token,
    idempotencyKey: input.idempotencyKey,
    body: {
      decision: input.decision,
      note: input.note,
    },
  });
}
