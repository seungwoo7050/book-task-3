import type { CatalogEntry, OfflineEvalCase, RecommendationResult } from "@study1-v0/shared";
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
