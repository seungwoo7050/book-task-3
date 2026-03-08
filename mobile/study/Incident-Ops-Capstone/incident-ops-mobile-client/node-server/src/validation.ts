import { z } from "zod";
import {
  APPROVAL_DECISIONS,
  INCIDENT_SEVERITIES,
  USER_ROLES,
  type ApprovalDecisionBody,
  type CreateIncidentRequest,
  type LoginRequest,
  type RequestResolutionBody
} from "../../problem/code/contracts/contracts";

export const loginRequestSchema = z.object({
  userId: z.string().min(1),
  role: z.enum(USER_ROLES)
});

export const createIncidentRequestSchema = z.object({
  title: z.string().min(1).max(120),
  description: z.string().max(1000).optional(),
  severity: z.enum(INCIDENT_SEVERITIES)
});

export const requestResolutionSchema = z.object({
  reason: z.string().min(3).max(300)
});

export const approvalDecisionSchema = z.object({
  decision: z.enum(APPROVAL_DECISIONS),
  note: z.string().max(300).optional()
});

export function parseLoginRequest(payload: unknown): LoginRequest {
  return loginRequestSchema.parse(payload);
}

export function parseCreateIncidentRequest(payload: unknown): CreateIncidentRequest {
  return createIncidentRequestSchema.parse(payload);
}

export function parseRequestResolution(payload: unknown): RequestResolutionBody {
  return requestResolutionSchema.parse(payload);
}

export function parseApprovalDecision(payload: unknown): ApprovalDecisionBody {
  return approvalDecisionSchema.parse(payload);
}

export function parsePagination(cursorRaw: string | null, limitRaw: string | null): {
  cursor: number | null;
  limit: number;
} {
  const limit = limitRaw ? Number(limitRaw) : 20;
  if (!Number.isInteger(limit) || limit < 1 || limit > 100) {
    throw new Error("invalid limit");
  }

  if (!cursorRaw) {
    return { cursor: null, limit };
  }

  const cursor = Number(cursorRaw);
  if (!Number.isInteger(cursor) || cursor < 1) {
    throw new Error("invalid cursor");
  }

  return { cursor, limit };
}
