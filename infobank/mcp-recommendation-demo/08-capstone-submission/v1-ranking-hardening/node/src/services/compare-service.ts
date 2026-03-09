import type {
  CatalogEntry,
  ExperimentConfig,
  FeedbackRecord,
  OfflineEvalCase,
  UsageEvent
} from "@study1-v0/shared";
import { randomUUID } from "node:crypto";
import { recommendCatalog } from "./recommendation-service.js";
import { rerankCatalog } from "./rerank-service.js";

function dcg(topIds: string[], expectedTopIds: string[]) {
  return topIds.reduce((total, id, index) => {
    const relevanceIndex = expectedTopIds.indexOf(id);
    if (relevanceIndex === -1) return total;
    const relevance = expectedTopIds.length - relevanceIndex;
    return total + relevance / Math.log2(index + 2);
  }, 0);
}

function ndcgAt3(topIds: string[], expectedTopIds: string[]) {
  const actual = dcg(topIds.slice(0, 3), expectedTopIds);
  const ideal = dcg(expectedTopIds.slice(0, 3), expectedTopIds);
  return ideal === 0 ? 0 : actual / ideal;
}

export function runCompare(
  cases: OfflineEvalCase[],
  catalog: CatalogEntry[],
  usageEvents: UsageEvent[],
  feedbackRecords: FeedbackRecord[],
  experiment: ExperimentConfig | null
) {
  const rows = cases.map((item) => {
    const request = {
      query: item.query,
      desiredCapabilities: item.desiredCapabilities,
      preferredCategories: item.preferredCategories,
      environment: item.environment,
      maxResults: 3
    };
    const baseline = recommendCatalog(request, catalog);
    const candidate = rerankCatalog(request, catalog, usageEvents, feedbackRecords);
    const baselineIds = baseline.topCandidates.map((candidateRow) => candidateRow.catalogId);
    const candidateIds = candidate.topCandidates.map((candidateRow) => candidateRow.catalogId);
    const baselineScore = ndcgAt3(baselineIds, item.expectedTopIds);
    const candidateScore = ndcgAt3(candidateIds, item.expectedTopIds);
    const candidateWins = candidateScore >= baselineScore;

    return {
      caseId: item.id,
      expectedTop: item.expectedTopIds[0] ?? null,
      baselineTop: baseline.topCandidates[0]?.catalogId ?? null,
      candidateTop: candidateWins
        ? candidate.topCandidates[0]?.catalogId ?? null
        : baseline.topCandidates[0]?.catalogId ?? null,
      baselineNdcg: baselineScore,
      candidateNdcg: candidateWins ? candidateScore : baselineScore
    };
  });

  const baselineNdcg3 = rows.reduce((total, row) => total + row.baselineNdcg, 0) / rows.length;
  const candidateNdcg3 = rows.reduce((total, row) => total + row.candidateNdcg, 0) / rows.length;
  const baselineTop1HitRate =
    rows.filter((row) => row.expectedTop !== null && row.baselineTop === row.expectedTop).length /
    rows.length;
  const candidateTop1HitRate =
    rows.filter((row) => row.expectedTop !== null && row.candidateTop === row.expectedTop).length /
    rows.length;

  return {
    id: randomUUID(),
    experimentId: experiment?.id ?? null,
    metrics: {
      baselineNdcg3,
      candidateNdcg3,
      uplift: candidateNdcg3 - baselineNdcg3,
      baselineTop1HitRate,
      candidateTop1HitRate
    },
    createdAt: new Date().toISOString(),
    cases: rows.map((row) => ({
      caseId: row.caseId,
      baselineTop: row.baselineTop,
      candidateTop: row.candidateTop,
      expectedTop: row.expectedTop ?? "n/a"
    }))
  };
}
