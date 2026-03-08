import type { CatalogEntry, OfflineEvalCase } from "@study1-v3/shared";
import { randomUUID } from "node:crypto";
import { recommendCatalog } from "./recommendation-service.js";

export function evaluateOfflineCases(cases: OfflineEvalCase[], catalog: CatalogEntry[]) {
  const evaluatedCases = cases.map((item) => {
    const result = recommendCatalog(
      {
        query: item.query,
        desiredCapabilities: item.desiredCapabilities,
        preferredCategories: item.preferredCategories,
        environment: item.environment,
        maxResults: 3
      },
      catalog
    );

    const topIds = result.topCandidates.map((candidate) => candidate.catalogId);
    const matchedExpected = item.expectedTopIds.filter((expectedId) => topIds.includes(expectedId));
    const forbiddenHits = item.forbiddenIds.filter((forbiddenId) => topIds.includes(forbiddenId));
    const explanationPass = item.requiredReasonTypes.every((requiredReason) =>
      result.topCandidates[0]?.trace.reasons.some((reason) => reason.type === requiredReason)
    );

    return {
      caseId: item.id,
      topIds,
      matchedExpected,
      forbiddenHits,
      explanationPass
    };
  });

  const metrics = {
    top3Recall:
      evaluatedCases.reduce(
        (total, item, index) =>
          total + item.matchedExpected.length / cases[index]!.expectedTopIds.length,
        0
      ) / evaluatedCases.length,
    explanationCompleteness:
      evaluatedCases.filter((item) => item.explanationPass).length / evaluatedCases.length,
    forbiddenHitRate:
      evaluatedCases.filter((item) => item.forbiddenHits.length > 0).length / evaluatedCases.length
  };

  return {
    id: randomUUID(),
    metrics,
    acceptance: {
      top3RecallPass: metrics.top3Recall >= 0.9,
      explanationPass: metrics.explanationCompleteness >= 1,
      forbiddenPass: metrics.forbiddenHitRate === 0
    },
    cases: evaluatedCases,
    createdAt: new Date().toISOString()
  };
}
