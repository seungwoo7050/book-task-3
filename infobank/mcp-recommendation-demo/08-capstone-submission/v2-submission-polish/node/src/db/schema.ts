import type {
  ArtifactExport,
  CatalogEntry,
  CompatibilityReport,
  ExperimentConfig,
  FeedbackRecord,
  OfflineEvalCase,
  RecommendationResult,
  ReleaseCandidate,
  ReleaseGateReport,
  UsageEvent
} from "@study1-v0/shared";
import { jsonb, pgTable, text, timestamp } from "drizzle-orm/pg-core";

export const catalogEntries = pgTable("catalog_entries", {
  id: text("id").primaryKey(),
  slug: text("slug").notNull(),
  payload: jsonb("payload").$type<CatalogEntry>().notNull(),
  createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull(),
  updatedAt: timestamp("updated_at", { withTimezone: true }).defaultNow().notNull()
});

export const evalCases = pgTable("eval_cases", {
  id: text("id").primaryKey(),
  payload: jsonb("payload").$type<OfflineEvalCase>().notNull(),
  createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull()
});

export const recommendationRuns = pgTable("recommendation_runs", {
  id: text("id").primaryKey(),
  payload: jsonb("payload").$type<RecommendationResult>().notNull(),
  createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull()
});

export const evalRuns = pgTable("eval_runs", {
  id: text("id").primaryKey(),
  payload: jsonb("payload")
    .$type<{
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
    }>()
    .notNull(),
  createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull()
});

export const usageEvents = pgTable("usage_events", {
  id: text("id").primaryKey(),
  payload: jsonb("payload").$type<UsageEvent>().notNull(),
  createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull()
});

export const feedbackRecords = pgTable("feedback_records", {
  id: text("id").primaryKey(),
  payload: jsonb("payload").$type<FeedbackRecord>().notNull(),
  createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull()
});

export const experiments = pgTable("experiments", {
  id: text("id").primaryKey(),
  payload: jsonb("payload").$type<ExperimentConfig>().notNull(),
  createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull(),
  updatedAt: timestamp("updated_at", { withTimezone: true }).defaultNow().notNull()
});

export const compareRuns = pgTable("compare_runs", {
  id: text("id").primaryKey(),
  payload: jsonb("payload")
    .$type<{
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
    }>()
    .notNull(),
  createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull()
});

export const releaseCandidates = pgTable("release_candidates", {
  id: text("id").primaryKey(),
  payload: jsonb("payload").$type<ReleaseCandidate>().notNull(),
  createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull(),
  updatedAt: timestamp("updated_at", { withTimezone: true }).defaultNow().notNull()
});

export const compatibilityReports = pgTable("compatibility_reports", {
  id: text("id").primaryKey(),
  payload: jsonb("payload").$type<CompatibilityReport>().notNull(),
  createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull()
});

export const gateReports = pgTable("gate_reports", {
  id: text("id").primaryKey(),
  payload: jsonb("payload").$type<ReleaseGateReport>().notNull(),
  createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull()
});

export const artifactExports = pgTable("artifact_exports", {
  id: text("id").primaryKey(),
  payload: jsonb("payload").$type<ArtifactExport>().notNull(),
  createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull()
});
