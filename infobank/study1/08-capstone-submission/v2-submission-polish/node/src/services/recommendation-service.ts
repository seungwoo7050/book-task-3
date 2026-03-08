import type {
  CatalogEntry,
  RecommendationRequest,
  RecommendationResult,
  RecommendationTrace
} from "@study1-v0/shared";
import { recommendationRequestSchema } from "@study1-v0/shared";
import semver from "semver";
import { randomUUID } from "node:crypto";

function tokenize(text: string) {
  return text
    .toLowerCase()
    .replace(/[^0-9a-zA-Z가-힣\s-]/g, " ")
    .split(/\s+/)
    .map((token) => token.trim())
    .filter((token) => token.length >= 2);
}

function unique(values: string[]) {
  return [...new Set(values)];
}

function getKeywords(entry: CatalogEntry) {
  return unique([
    entry.name,
    entry.summaryKo,
    entry.descriptionKo,
    entry.toolCategory,
    ...entry.capabilities,
    ...entry.koreanUseCases,
    ...entry.differentiationPoints,
    ...entry.tags,
    ...entry.exposure.recommendedFor
  ]).map((value) => value.toLowerCase());
}

function calculateIntentScore(queryTokens: string[], entry: CatalogEntry) {
  const keywords = getKeywords(entry);
  let hits = 0;

  for (const token of queryTokens) {
    if (keywords.some((keyword) => keyword.includes(token) || token.includes(keyword))) {
      hits += 1;
    }
  }

  return Math.min(35, hits * 6);
}

function calculateCapabilityScore(request: RecommendationRequest, entry: CatalogEntry) {
  if (request.desiredCapabilities.length === 0) {
    return 12;
  }

  const matches = request.desiredCapabilities.filter((capability) =>
    entry.capabilities.includes(capability)
  ).length;

  return (matches / request.desiredCapabilities.length) * 35;
}

function calculateCategoryScore(request: RecommendationRequest, entry: CatalogEntry) {
  return request.preferredCategories.includes(entry.toolCategory) ? 10 : 0;
}

function calculateLocaleScore(request: RecommendationRequest, entry: CatalogEntry) {
  const locale = request.environment.locale.toLowerCase();
  const matched = entry.supportedLocales.some((supported) =>
    supported.toLowerCase().startsWith(locale.slice(0, 2))
  );
  return matched ? 10 : -5;
}

function calculateCompatibilityScore(request: RecommendationRequest, entry: CatalogEntry) {
  const transportMatch = entry.runtime.transports.includes(request.environment.transport);
  const platformMatch = entry.runtime.platforms.includes(request.environment.platform);
  const versionMatch =
    semver.gte(request.environment.clientVersion, entry.compatibility.minimumClientVersion) &&
    semver.lte(request.environment.clientVersion, entry.compatibility.maximumClientVersion);

  return transportMatch && platformMatch && versionMatch ? 15 : -20;
}

function calculateMaturityScore(entry: CatalogEntry) {
  return entry.maturity.score / 10;
}

function calculateFreshnessScore(entry: CatalogEntry) {
  return entry.freshnessScore * 5;
}

export function scoreCatalogEntry(requestInput: RecommendationRequest, entry: CatalogEntry) {
  const request = recommendationRequestSchema.parse(requestInput);
  const queryTokens = tokenize(request.query);

  const breakdown = {
    intent: calculateIntentScore(queryTokens, entry),
    capability: calculateCapabilityScore(request, entry),
    category: calculateCategoryScore(request, entry),
    locale: calculateLocaleScore(request, entry),
    compatibility: calculateCompatibilityScore(request, entry),
    maturity: calculateMaturityScore(entry),
    freshness: calculateFreshnessScore(entry)
  };

  const reasons: RecommendationTrace["reasons"] = [
    {
      type: "capabilityMatch",
      label: "capability",
      score: breakdown.capability,
      detailKo: `${request.desiredCapabilities.filter((capability) => entry.capabilities.includes(capability)).join(", ") || entry.capabilities.slice(0, 2).join(", ")} 역량이 직접 맞습니다.`
    },
    {
      type: "differentiation",
      label: "differentiation",
      score: 8,
      detailKo: entry.differentiationPoints[0] ?? entry.exposure.userFacingSummaryKo
    },
    {
      type: "compatibility",
      label: "compatibility",
      score: breakdown.compatibility,
      detailKo: `현재 클라이언트 ${request.environment.clientVersion} / ${request.environment.transport} / ${request.environment.platform} 환경과 호환됩니다.`
    },
    {
      type: "localeFit",
      label: "locale",
      score: breakdown.locale,
      detailKo: `${request.environment.locale} 기준 한국어 설명 흐름을 바로 사용할 수 있습니다.`
    },
    {
      type: "maturity",
      label: "maturity",
      score: breakdown.maturity,
      detailKo: `${entry.maturity.stage} 단계로 운영 안정성이 비교적 높습니다.`
    }
  ];

  return {
    totalScore:
      breakdown.intent +
      breakdown.capability +
      breakdown.category +
      breakdown.locale +
      breakdown.compatibility +
      breakdown.maturity +
      breakdown.freshness,
    breakdown,
    reasons
  };
}

export function buildExplanationKo(
  entry: CatalogEntry,
  request: RecommendationRequest,
  trace: RecommendationTrace
) {
  const capabilityReason =
    trace.reasons.find((reason) => reason.type === "capabilityMatch")?.detailKo ??
    `${entry.capabilities.slice(0, 2).join(", ")} 역량이 맞습니다.`;
  const differentiationReason =
    trace.reasons.find((reason) => reason.type === "differentiation")?.detailKo ??
    entry.differentiationPoints[0];
  const compatibilityReason =
    trace.reasons.find((reason) => reason.type === "compatibility")?.detailKo ??
    `현재 클라이언트 ${request.environment.clientVersion} 환경과 호환됩니다.`;

  return `${entry.name}는 ${capabilityReason} ${differentiationReason} ${compatibilityReason}`;
}

export function recommendCatalog(
  requestInput: RecommendationRequest,
  catalog: CatalogEntry[]
): RecommendationResult {
  const request = recommendationRequestSchema.parse(requestInput);

  const ranked = catalog
    .map((entry) => {
      const scored = scoreCatalogEntry(request, entry);
      const trace: RecommendationTrace = {
        candidateId: entry.id,
        totalScore: scored.totalScore,
        breakdown: scored.breakdown,
        reasons: scored.reasons
      };

      return {
        catalogId: entry.id,
        rank: 0,
        score: scored.totalScore,
        explanationKo: buildExplanationKo(entry, request, trace),
        trace
      };
    })
    .sort((left, right) => right.score - left.score || left.catalogId.localeCompare(right.catalogId))
    .slice(0, request.maxResults)
    .map((candidate, index) => ({
      ...candidate,
      rank: index + 1
    }));

  return {
    requestId: randomUUID(),
    createdAt: new Date().toISOString(),
    request,
    topCandidates: ranked
  };
}
