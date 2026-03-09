import type { AuditEvent, StoredUser } from "@study1-v3/shared";
import { randomUUID } from "node:crypto";

export function buildAuditEvent(args: {
  actor: StoredUser | null;
  action: string;
  targetType: string;
  targetId?: string | null;
  detailKo: string;
  metadata?: Record<string, unknown>;
}): AuditEvent {
  return {
    id: randomUUID(),
    actorUserId: args.actor?.id ?? null,
    actorEmail: args.actor?.email ?? null,
    action: args.action,
    targetType: args.targetType,
    targetId: args.targetId ?? null,
    detailKo: args.detailKo,
    metadata: args.metadata ?? {},
    createdAt: new Date().toISOString()
  };
}
