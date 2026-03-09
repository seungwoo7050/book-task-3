import type {
  CatalogEntry,
  ExperimentConfig,
  FeedbackRecord,
  OfflineEvalCase,
  RecommendationResult,
  UsageEvent
} from "@study1-v0/shared";
import { desc, eq } from "drizzle-orm";
import { db } from "../db/client.js";
import {
  catalogEntries,
  compareRuns,
  evalCases,
  evalRuns,
  experiments,
  feedbackRecords,
  recommendationRuns,
  usageEvents
} from "../db/schema.js";

export async function listCatalogEntries(): Promise<CatalogEntry[]> {
  const rows = await db.select().from(catalogEntries).orderBy(catalogEntries.slug);
  return rows.map((row) => row.payload);
}

export async function getCatalogEntryById(id: string): Promise<CatalogEntry | null> {
  const [row] = await db.select().from(catalogEntries).where(eq(catalogEntries.id, id)).limit(1);
  return row?.payload ?? null;
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
