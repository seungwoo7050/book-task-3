import type {
  ArtifactExport,
  AuditEvent,
  CatalogEntry,
  CatalogImportBundle,
  CompatibilityReport,
  ExperimentConfig,
  FeedbackRecord,
  InstanceSettings,
  JobRun,
  OfflineEvalCase,
  RecommendationResult,
  ReleaseCandidate,
  ReleaseGateReport,
  Session,
  StoredUser,
  UsageEvent,
  User
} from "@study1-v3/shared";
import { desc, eq } from "drizzle-orm";
import { db } from "../db/client.js";
import {
  artifactExports,
  auditLogs,
  catalogEntries,
  compatibilityReports,
  compareRuns,
  evalCases,
  evalRuns,
  experiments,
  feedbackRecords,
  gateReports,
  instanceSettings,
  jobRuns,
  releaseCandidates,
  recommendationRuns,
  sessions,
  usageEvents,
  users
} from "../db/schema.js";

function toPublicUser(user: StoredUser): User {
  const { passwordHash: _passwordHash, ...rest } = user;
  return rest;
}

export async function listCatalogEntries(): Promise<CatalogEntry[]> {
  const rows = await db.select().from(catalogEntries).orderBy(catalogEntries.slug);
  return rows.map((row) => row.payload);
}

export async function getCatalogEntryById(id: string): Promise<CatalogEntry | null> {
  const [row] = await db.select().from(catalogEntries).where(eq(catalogEntries.id, id)).limit(1);
  return row?.payload ?? null;
}

export async function createCatalogEntry(entry: CatalogEntry) {
  await db.insert(catalogEntries).values({
    id: entry.id,
    slug: entry.slug,
    payload: entry
  });
}

export async function updateCatalogEntry(entry: CatalogEntry) {
  await db
    .update(catalogEntries)
    .set({
      slug: entry.slug,
      payload: entry,
      updatedAt: new Date()
    })
    .where(eq(catalogEntries.id, entry.id));
}

export async function deleteCatalogEntry(id: string) {
  await db.delete(catalogEntries).where(eq(catalogEntries.id, id));
}

export async function listEvalCases(): Promise<OfflineEvalCase[]> {
  const rows = await db.select().from(evalCases).orderBy(evalCases.id);
  return rows.map((row) => row.payload);
}

export async function saveRecommendationRun(result: RecommendationResult) {
  await db.insert(recommendationRuns).values({
    id: result.requestId,
    payload: result
  });
}

export async function saveEvalRun(summary: {
  id: string;
  metrics: {
    top3Recall: number;
    explanationCompleteness: number;
    forbiddenHitRate: number;
  };
  acceptance: {
    top3RecallPass: boolean;
    explanationPass: boolean;
    forbiddenPass: boolean;
  };
  cases: Array<{
    caseId: string;
    topIds: string[];
    matchedExpected: string[];
    forbiddenHits: string[];
    explanationPass: boolean;
  }>;
  createdAt: string;
}) {
  await db.insert(evalRuns).values({
    id: summary.id,
    payload: summary
  });
}

export async function getLatestEvalRun() {
  const [row] = await db.select().from(evalRuns).orderBy(desc(evalRuns.createdAt)).limit(1);
  return row?.payload ?? null;
}

export async function listUsageEvents(): Promise<UsageEvent[]> {
  const rows = await db.select().from(usageEvents).orderBy(desc(usageEvents.createdAt));
  return rows.map((row) => row.payload);
}

export async function createUsageEvent(event: UsageEvent) {
  await db.insert(usageEvents).values({
    id: event.id,
    payload: event
  });
}

export async function listFeedbackRecords(): Promise<FeedbackRecord[]> {
  const rows = await db.select().from(feedbackRecords).orderBy(desc(feedbackRecords.createdAt));
  return rows.map((row) => row.payload);
}

export async function createFeedbackRecord(record: FeedbackRecord) {
  await db.insert(feedbackRecords).values({
    id: record.id,
    payload: record
  });
}

export async function listExperiments(): Promise<ExperimentConfig[]> {
  const rows = await db.select().from(experiments).orderBy(desc(experiments.updatedAt));
  return rows.map((row) => row.payload);
}

export async function createExperiment(config: ExperimentConfig) {
  await db.insert(experiments).values({
    id: config.id,
    payload: config
  });
}

export async function updateExperiment(config: ExperimentConfig) {
  await db
    .update(experiments)
    .set({
      payload: config,
      updatedAt: new Date()
    })
    .where(eq(experiments.id, config.id));
}

export async function deleteExperiment(id: string) {
  await db.delete(experiments).where(eq(experiments.id, id));
}

export async function saveCompareRun(summary: {
  id: string;
  experimentId: string | null;
  metrics: {
    baselineNdcg3: number;
    candidateNdcg3: number;
    uplift: number;
    baselineTop1HitRate: number;
    candidateTop1HitRate: number;
  };
  createdAt: string;
  cases: Array<{
    caseId: string;
    baselineTop: string | null;
    candidateTop: string | null;
    expectedTop: string;
  }>;
}) {
  await db.insert(compareRuns).values({
    id: summary.id,
    payload: summary
  });
}

export async function getLatestCompareRun() {
  const [row] = await db.select().from(compareRuns).orderBy(desc(compareRuns.createdAt)).limit(1);
  return row?.payload ?? null;
}

export async function listReleaseCandidates(): Promise<ReleaseCandidate[]> {
  const rows = await db.select().from(releaseCandidates).orderBy(desc(releaseCandidates.updatedAt));
  return rows.map((row) => row.payload);
}

export async function getReleaseCandidateById(id: string): Promise<ReleaseCandidate | null> {
  const [row] = await db.select().from(releaseCandidates).where(eq(releaseCandidates.id, id)).limit(1);
  return row?.payload ?? null;
}

export async function createReleaseCandidate(candidate: ReleaseCandidate) {
  await db.insert(releaseCandidates).values({
    id: candidate.id,
    payload: candidate
  });
}

export async function updateReleaseCandidate(candidate: ReleaseCandidate) {
  await db
    .update(releaseCandidates)
    .set({
      payload: candidate,
      updatedAt: new Date()
    })
    .where(eq(releaseCandidates.id, candidate.id));
}

export async function deleteReleaseCandidate(id: string) {
  await db.delete(releaseCandidates).where(eq(releaseCandidates.id, id));
}

export async function saveCompatibilityReport(report: CompatibilityReport) {
  await db.insert(compatibilityReports).values({
    id: report.id,
    payload: report
  });
}

export async function getLatestCompatibilityReport() {
  const [row] = await db
    .select()
    .from(compatibilityReports)
    .orderBy(desc(compatibilityReports.createdAt))
    .limit(1);
  return row?.payload ?? null;
}

export async function saveGateReport(report: ReleaseGateReport) {
  await db.insert(gateReports).values({
    id: report.id,
    payload: report
  });
}

export async function getLatestGateReport() {
  const [row] = await db.select().from(gateReports).orderBy(desc(gateReports.createdAt)).limit(1);
  return row?.payload ?? null;
}

export async function saveArtifactExport(artifact: ArtifactExport) {
  await db.insert(artifactExports).values({
    id: artifact.id,
    payload: artifact
  });
}

export async function getLatestArtifactExport() {
  const [row] = await db
    .select()
    .from(artifactExports)
    .orderBy(desc(artifactExports.createdAt))
    .limit(1);
  return row?.payload ?? null;
}

export async function listUsers(): Promise<User[]> {
  const rows = await db.select().from(users).orderBy(users.email);
  return rows.map((row) => toPublicUser(row.payload));
}

export async function getStoredUserByEmail(email: string): Promise<StoredUser | null> {
  const [row] = await db.select().from(users).where(eq(users.email, email)).limit(1);
  return row?.payload ?? null;
}

export async function getStoredUserById(id: string): Promise<StoredUser | null> {
  const [row] = await db.select().from(users).where(eq(users.id, id)).limit(1);
  return row?.payload ?? null;
}

export async function saveStoredUser(user: StoredUser) {
  await db
    .insert(users)
    .values({
      id: user.id,
      email: user.email,
      role: user.role,
      isActive: user.isActive,
      payload: user
    })
    .onConflictDoUpdate({
      target: users.id,
      set: {
        email: user.email,
        role: user.role,
        isActive: user.isActive,
        payload: user,
        updatedAt: new Date()
      }
    });
}

export async function createSessionRecord(session: Session, tokenHash: string) {
  await db.insert(sessions).values({
    id: session.id,
    userId: session.userId,
    tokenHash,
    payload: session,
    expiresAt: new Date(session.expiresAt)
  });
}

export async function getSessionRecordByTokenHash(tokenHash: string) {
  const [row] = await db.select().from(sessions).where(eq(sessions.tokenHash, tokenHash)).limit(1);
  return row ?? null;
}

export async function deleteSessionById(id: string) {
  await db.delete(sessions).where(eq(sessions.id, id));
}

export async function touchSession(session: Session) {
  await db
    .update(sessions)
    .set({
      payload: session,
      expiresAt: new Date(session.expiresAt),
      updatedAt: new Date()
    })
    .where(eq(sessions.id, session.id));
}

export async function purgeExpiredSessions() {
  const rows = await db.select().from(sessions);
  const expiredIds = rows
    .filter((row) => row.expiresAt.getTime() <= Date.now())
    .map((row) => row.id);

  for (const id of expiredIds) {
    await db.delete(sessions).where(eq(sessions.id, id));
  }
}

export async function getInstanceSettings(): Promise<InstanceSettings | null> {
  const [row] = await db
    .select()
    .from(instanceSettings)
    .where(eq(instanceSettings.id, "default"))
    .limit(1);
  return row?.payload ?? null;
}

export async function saveInstanceSettings(settings: InstanceSettings) {
  await db
    .insert(instanceSettings)
    .values({
      id: settings.id,
      payload: settings
    })
    .onConflictDoUpdate({
      target: instanceSettings.id,
      set: {
        payload: settings,
        updatedAt: new Date()
      }
    });
}

export async function createAuditEvent(event: AuditEvent) {
  await db.insert(auditLogs).values({
    id: event.id,
    actorUserId: event.actorUserId,
    action: event.action,
    targetType: event.targetType,
    targetId: event.targetId,
    payload: event
  });
}

export async function listAuditEvents(): Promise<AuditEvent[]> {
  const rows = await db.select().from(auditLogs).orderBy(desc(auditLogs.createdAt)).limit(100);
  return rows.map((row) => row.payload);
}

export async function createJobRun(run: JobRun) {
  await db.insert(jobRuns).values({
    id: run.id,
    name: run.name,
    status: run.status,
    payload: run
  });
}

export async function getJobRunById(id: string): Promise<JobRun | null> {
  const [row] = await db.select().from(jobRuns).where(eq(jobRuns.id, id)).limit(1);
  return row?.payload ?? null;
}

export async function listRecentJobRuns(): Promise<JobRun[]> {
  const rows = await db.select().from(jobRuns).orderBy(desc(jobRuns.createdAt)).limit(25);
  return rows.map((row) => row.payload);
}

export async function updateJobRun(run: JobRun) {
  await db
    .update(jobRuns)
    .set({
      name: run.name,
      status: run.status,
      payload: run,
      updatedAt: new Date()
    })
    .where(eq(jobRuns.id, run.id));
}

export async function upsertCatalogImportBundle(bundle: CatalogImportBundle) {
  await db.transaction(async (tx) => {
    for (const entry of bundle.catalogEntries) {
      await tx
        .insert(catalogEntries)
        .values({
          id: entry.id,
          slug: entry.slug,
          payload: entry
        })
        .onConflictDoUpdate({
          target: catalogEntries.id,
          set: {
            slug: entry.slug,
            payload: entry,
            updatedAt: new Date()
          }
        });
    }

    for (const item of bundle.evalCases ?? []) {
      await tx
        .insert(evalCases)
        .values({
          id: item.id,
          payload: item
        })
        .onConflictDoUpdate({
          target: evalCases.id,
          set: {
            payload: item
          }
        });
    }

    for (const candidate of bundle.releaseCandidates ?? []) {
      await tx
        .insert(releaseCandidates)
        .values({
          id: candidate.id,
          payload: candidate
        })
        .onConflictDoUpdate({
          target: releaseCandidates.id,
          set: {
            payload: candidate,
            updatedAt: new Date()
          }
        });
    }
  });
}

export async function exportCatalogImportBundle(): Promise<CatalogImportBundle> {
  const [catalog, cases, candidates] = await Promise.all([
    listCatalogEntries(),
    listEvalCases(),
    listReleaseCandidates()
  ]);

  return {
    catalogEntries: catalog,
    evalCases: cases,
    releaseCandidates: candidates
  };
}
