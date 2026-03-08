import type { CatalogEntry, OfflineEvalCase, RecommendationResult } from "@study1-v0/shared";
import { desc, eq } from "drizzle-orm";
import { db } from "../db/client.js";
import { catalogEntries, evalCases, evalRuns, recommendationRuns } from "../db/schema.js";

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
