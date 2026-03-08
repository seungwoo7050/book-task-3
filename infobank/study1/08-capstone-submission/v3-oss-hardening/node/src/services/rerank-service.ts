import type { CatalogEntry, FeedbackRecord, RecommendationRequest, UsageEvent } from "@study1-v3/shared";
import type { RecommendationTrace } from "@study1-v3/shared";
import { recommendCatalog, scoreCatalogEntry } from "./recommendation-service.js";

export function aggregateSignals(usageEvents: UsageEvent[], feedbackRecords: FeedbackRecord[]) {
  const eventMap = new Map<
    string,
    {
      impressions: number;
      clicks: number;
      accepts: number;
      dismisses: number;
      feedbackTotal: number;
      feedbackCount: number;
    }
  >();

  for (const event of usageEvents) {
    const current = eventMap.get(event.catalogId) ?? {
      impressions: 0,
      clicks: 0,
      accepts: 0,
      dismisses: 0,
      feedbackTotal: 0,
      feedbackCount: 0
    };

    if (event.action === "impression") current.impressions += 1;
    if (event.action === "click") current.clicks += 1;
    if (event.action === "accept") current.accepts += 1;
    if (event.action === "dismiss") current.dismisses += 1;
    eventMap.set(event.catalogId, current);
  }

  for (const feedback of feedbackRecords) {
    const current = eventMap.get(feedback.catalogId) ?? {
      impressions: 0,
      clicks: 0,
      accepts: 0,
      dismisses: 0,
      feedbackTotal: 0,
      feedbackCount: 0
    };

    current.feedbackTotal += feedback.scoreDelta;
    current.feedbackCount += 1;
    eventMap.set(feedback.catalogId, current);
  }

  return eventMap;
}

export function rerankCatalog(
  request: RecommendationRequest,
  catalog: CatalogEntry[],
  usageEvents: UsageEvent[],
  feedbackRecords: FeedbackRecord[]
) {
  const baseline = recommendCatalog({ ...request, maxResults: Math.max(request.maxResults, 5) }, catalog);
  const signals = aggregateSignals(usageEvents, feedbackRecords);

  const reranked = baseline.topCandidates
    .map((candidate) => {
      const entry = catalog.find((item) => item.id === candidate.catalogId)!;
      const signal = signals.get(candidate.catalogId) ?? {
        impressions: 0,
        clicks: 0,
        accepts: 0,
        dismisses: 0,
        feedbackTotal: 0,
        feedbackCount: 0
      };

      const impressions = signal.impressions || 1;
      const ctr = signal.clicks / impressions;
      const acceptRate = signal.accepts / impressions;
      const feedbackAverage =
        signal.feedbackCount > 0 ? signal.feedbackTotal / signal.feedbackCount : 0;
      const explanationQuality = entry.supportedLocales.includes("ko-KR") ? 1 : 0.3;
      const freshness = entry.freshnessScore;
      const uplift =
        ctr * 14 + acceptRate * 18 + feedbackAverage * 5 + explanationQuality * 4 + freshness * 2;

      const rescored = scoreCatalogEntry(request, entry);
      const trace: RecommendationTrace = {
        candidateId: candidate.catalogId,
        totalScore: rescored.totalScore + uplift,
        breakdown: rescored.breakdown,
        reasons: [
          ...candidate.trace.reasons,
          {
            type: "maturity",
            label: "rerank-signal",
            score: uplift,
            detailKo: `실사용 신호(CTR ${(ctr * 100).toFixed(0)}%, accept ${(acceptRate * 100).toFixed(0)}%, feedback ${feedbackAverage.toFixed(1)})가 candidate 점수를 끌어올립니다.`
          }
        ]
      };

      return {
        ...candidate,
        score: trace.totalScore,
        trace,
        explanationKo: `${candidate.explanationKo} 실사용 신호 기준으로도 우선순위가 강화되었습니다.`
      };
    })
    .sort((left, right) => right.score - left.score || left.catalogId.localeCompare(right.catalogId))
    .slice(0, request.maxResults)
    .map((candidate, index) => ({
      ...candidate,
      rank: index + 1
    }));

  return {
    ...baseline,
    requestId: `candidate-${baseline.requestId}`,
    topCandidates: reranked
  };
}
