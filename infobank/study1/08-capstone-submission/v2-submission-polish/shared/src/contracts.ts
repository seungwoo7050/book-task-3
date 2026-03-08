import { z } from "zod";

export const toolCategorySchema = z.enum([
  "code",
  "data",
  "docs",
  "browser",
  "design",
  "communication",
  "productivity",
  "ops",
  "analytics",
  "support"
]);

export const transportSchema = z.enum(["stdio", "http"]);
export const platformSchema = z.enum(["node", "browser", "hybrid"]);
export const reasonTypeSchema = z.enum([
  "capabilityMatch",
  "differentiation",
  "compatibility",
  "localeFit",
  "maturity"
]);

export const mcpManifestSchema = z.object({
  id: z.string().min(1),
  slug: z.string().min(1),
  name: z.string().min(1),
  version: z.string().min(1),
  toolCategory: toolCategorySchema,
  summaryKo: z.string().min(10),
  descriptionKo: z.string().min(20),
  capabilities: z.array(z.string().min(2)).min(3),
  koreanUseCases: z.array(z.string().min(4)).min(2),
  differentiationPoints: z.array(z.string().min(8)).min(2),
  supportedLocales: z.array(z.string().min(2)).min(1),
  runtime: z.object({
    protocolVersion: z.string().min(1),
    nodeRange: z.string().min(1),
    transports: z.array(transportSchema).min(1),
    platforms: z.array(platformSchema).min(1)
  }),
  maturity: z.object({
    stage: z.enum(["pilot", "validated", "production"]),
    score: z.number().int().min(0).max(100)
  }),
  compatibility: z.object({
    minimumClientVersion: z.string().min(1),
    maximumClientVersion: z.string().min(1),
    testedClientVersions: z.array(z.string().min(1)).min(1),
    deprecatedClientVersions: z.array(z.string().min(1)),
    breakingChanges: z.array(z.string())
  }),
  operational: z.object({
    maintainer: z.string().min(2),
    slaTier: z.enum(["community", "business", "mission-critical"]),
    securityReview: z.boolean(),
    releaseChannel: z.enum(["stable", "preview"])
  }),
  tags: z.array(z.string().min(2)).min(2),
  freshnessScore: z.number().min(0).max(1)
});

export const catalogEntrySchema = mcpManifestSchema.extend({
  exposure: z.object({
    userFacingSummaryKo: z.string().min(10),
    recommendedFor: z.array(z.string().min(4)).min(2),
    cautionKo: z.string().min(8)
  })
});

export const recommendationRequestSchema = z.object({
  query: z.string().min(6),
  desiredCapabilities: z.array(z.string()).default([]),
  preferredCategories: z.array(toolCategorySchema).default([]),
  environment: z.object({
    locale: z.string().min(2),
    clientVersion: z.string().min(1),
    transport: transportSchema,
    platform: platformSchema
  }),
  maxResults: z.number().int().min(1).max(10).default(3)
});

export const reasonTraceSchema = z.object({
  type: reasonTypeSchema,
  label: z.string().min(2),
  score: z.number(),
  detailKo: z.string().min(4)
});

export const recommendationTraceSchema = z.object({
  candidateId: z.string().min(1),
  totalScore: z.number(),
  breakdown: z.object({
    intent: z.number(),
    capability: z.number(),
    category: z.number(),
    locale: z.number(),
    compatibility: z.number(),
    maturity: z.number(),
    freshness: z.number()
  }),
  reasons: z.array(reasonTraceSchema).min(3)
});

export const recommendationCandidateSchema = z.object({
  catalogId: z.string().min(1),
  rank: z.number().int().min(1),
  score: z.number(),
  explanationKo: z.string().min(12),
  trace: recommendationTraceSchema
});

export const recommendationResultSchema = z.object({
  requestId: z.string().min(1),
  createdAt: z.string().min(1),
  request: recommendationRequestSchema,
  topCandidates: z.array(recommendationCandidateSchema).min(1)
});

export const offlineEvalCaseSchema = z.object({
  id: z.string().min(1),
  title: z.string().min(4),
  query: z.string().min(6),
  desiredCapabilities: z.array(z.string()).min(1),
  preferredCategories: z.array(toolCategorySchema),
  expectedTopIds: z.array(z.string()).min(1),
  forbiddenIds: z.array(z.string()),
  requiredReasonTypes: z.array(reasonTypeSchema).min(1),
  environment: recommendationRequestSchema.shape.environment,
  notesKo: z.string().min(8)
});

export const usageEventSchema = z.object({
  id: z.string().min(1),
  recommendationRunId: z.string().min(1),
  catalogId: z.string().min(1),
  action: z.enum(["impression", "click", "accept", "dismiss"]),
  actor: z.enum(["user", "operator"]),
  createdAt: z.string().min(1),
  metadata: z.record(z.string(), z.string()).default({})
});

export const feedbackRecordSchema = z.object({
  id: z.string().min(1),
  recommendationRunId: z.string().min(1),
  catalogId: z.string().min(1),
  scoreDelta: z.number().int().min(-2).max(2),
  noteKo: z.string().min(4),
  reviewer: z.string().min(2),
  createdAt: z.string().min(1)
});

export const experimentConfigSchema = z.object({
  id: z.string().min(1),
  name: z.string().min(3),
  baselineStrategy: z.string().min(2),
  candidateStrategy: z.string().min(2),
  trafficSplitPercent: z.number().int().min(0).max(100),
  status: z.enum(["draft", "running", "completed"]),
  hypothesisKo: z.string().min(8)
});

export const releaseCandidateSchema = z.object({
  id: z.string().min(1),
  name: z.string().min(3),
  manifestId: z.string().min(1),
  previousVersion: z.string().min(1),
  releaseVersion: z.string().min(1),
  targetClientVersion: z.string().min(1),
  releaseNotesKo: z.string().min(20),
  requiredDocs: z.array(z.string().min(4)).min(1),
  requiredArtifacts: z.array(z.string().min(4)).min(1),
  deprecatedFieldsUsed: z.array(z.string()),
  owner: z.string().min(2),
  status: z.enum(["draft", "candidate", "approved", "rejected"]),
  createdAt: z.string().min(1),
  updatedAt: z.string().min(1)
});

export const compatibilityReportSchema = z.object({
  id: z.string().min(1),
  releaseCandidateId: z.string().min(1),
  candidateVersion: z.string().min(1),
  passed: z.boolean(),
  checks: z.array(
    z.object({
      name: z.string().min(2),
      passed: z.boolean(),
      detailKo: z.string().min(4)
    })
  ),
  issues: z.array(z.string()),
  checkedAt: z.string().min(1)
});

export const releaseGateReportSchema = z.object({
  id: z.string().min(1),
  releaseCandidateId: z.string().min(1),
  passed: z.boolean(),
  reasons: z.array(z.string()),
  metrics: z.object({
    top3Recall: z.number(),
    explanationCompleteness: z.number(),
    forbiddenHitRate: z.number(),
    baselineNdcg3: z.number(),
    candidateNdcg3: z.number(),
    uplift: z.number()
  }),
  checkedAt: z.string().min(1)
});

export const artifactExportSchema = z.object({
  id: z.string().min(1),
  releaseCandidateId: z.string().min(1),
  format: z.enum(["markdown", "json"]),
  content: z.string().min(20),
  createdAt: z.string().min(1)
});

export type MCPManifest = z.infer<typeof mcpManifestSchema>;
export type CatalogEntry = z.infer<typeof catalogEntrySchema>;
export type RecommendationRequest = z.infer<typeof recommendationRequestSchema>;
export type RecommendationTrace = z.infer<typeof recommendationTraceSchema>;
export type RecommendationResult = z.infer<typeof recommendationResultSchema>;
export type OfflineEvalCase = z.infer<typeof offlineEvalCaseSchema>;
export type UsageEvent = z.infer<typeof usageEventSchema>;
export type FeedbackRecord = z.infer<typeof feedbackRecordSchema>;
export type ExperimentConfig = z.infer<typeof experimentConfigSchema>;
export type ReleaseCandidate = z.infer<typeof releaseCandidateSchema>;
export type CompatibilityReport = z.infer<typeof compatibilityReportSchema>;
export type ReleaseGateReport = z.infer<typeof releaseGateReportSchema>;
export type ArtifactExport = z.infer<typeof artifactExportSchema>;
