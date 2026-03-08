import type {
  ArtifactExport,
  AuditEvent,
  CatalogEntry,
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
  UsageEvent
} from "@study1-v3/shared";
import { boolean, jsonb, pgTable, text, timestamp } from "drizzle-orm/pg-core";

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

export const users = pgTable("users", {
  id: text("id").primaryKey(),
  email: text("email").notNull().unique(),
  role: text("role").notNull(),
  isActive: boolean("is_active").notNull().default(true),
  payload: jsonb("payload").$type<StoredUser>().notNull(),
  createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull(),
  updatedAt: timestamp("updated_at", { withTimezone: true }).defaultNow().notNull()
});

export const sessions = pgTable("sessions", {
  id: text("id").primaryKey(),
  userId: text("user_id").notNull(),
  tokenHash: text("token_hash").notNull().unique(),
  payload: jsonb("payload").$type<Session>().notNull(),
  expiresAt: timestamp("expires_at", { withTimezone: true }).notNull(),
  createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull(),
  updatedAt: timestamp("updated_at", { withTimezone: true }).defaultNow().notNull()
});

export const instanceSettings = pgTable("instance_settings", {
  id: text("id").primaryKey(),
  payload: jsonb("payload").$type<InstanceSettings>().notNull(),
  updatedAt: timestamp("updated_at", { withTimezone: true }).defaultNow().notNull()
});

export const auditLogs = pgTable("audit_logs", {
  id: text("id").primaryKey(),
  actorUserId: text("actor_user_id"),
  action: text("action").notNull(),
  targetType: text("target_type").notNull(),
  targetId: text("target_id"),
  payload: jsonb("payload").$type<AuditEvent>().notNull(),
  createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull()
});

export const jobRuns = pgTable("job_runs", {
  id: text("id").primaryKey(),
  name: text("name").notNull(),
  status: text("status").notNull(),
  payload: jsonb("payload").$type<JobRun>().notNull(),
  createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull(),
  updatedAt: timestamp("updated_at", { withTimezone: true }).defaultNow().notNull()
});
