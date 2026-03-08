import {
  defaultDemoRuntimeConfig,
  defaultIssueQuery,
} from "@/lib/constants";
import { applyBulkPatch, applyIssuePatch } from "@/lib/optimistic";
import { createDashboardSummary, applyIssueQuery } from "@/lib/query";
import { bulkIssuePatchSchema, issuePatchSchema } from "@/lib/schemas";
import { createRetryableError, shouldSimulateFailure, waitForLatency } from "@/lib/simulate";
import {
  readIssues,
  readRuntimeConfig,
  readSavedViews,
  resetIssues,
  updateRuntimeConfig,
  writeIssues,
} from "@/lib/storage";
import {
  type BulkIssuePatch,
  type DashboardSummary,
  type DemoRuntimeConfig,
  type Issue,
  type IssueListResult,
  type IssuePatch,
  type IssueQuery,
  type SavedView,
} from "@/lib/types";
import { cloneValue } from "@/lib/utils";

async function simulateRequest(kind: "read" | "write"): Promise<void> {
  const config = readRuntimeConfig();
  await waitForLatency(config.latencyMs);

  if (shouldSimulateFailure(config)) {
    if (config.failNextRequest) {
      updateRuntimeConfig({ failNextRequest: false });
    }

    throw createRetryableError();
  }

  if (kind === "write" && config.failNextRequest) {
    updateRuntimeConfig({ failNextRequest: false });
  }
}

export async function listIssues(query: IssueQuery = defaultIssueQuery): Promise<IssueListResult> {
  await simulateRequest("read");
  return applyIssueQuery(readIssues(), query);
}

export async function getIssue(issueId: string): Promise<Issue | undefined> {
  await simulateRequest("read");
  return readIssues().find((issue) => issue.id === issueId);
}

export async function updateIssue(
  issueId: string,
  patch: IssuePatch,
): Promise<{ issue: Issue; previousIssue: Issue }> {
  const parsedPatch = issuePatchSchema.parse(patch);
  await simulateRequest("write");

  const issues = readIssues();
  const previousIssue = issues.find((issue) => issue.id === issueId);

  if (!previousIssue) {
    throw new Error(`Issue ${issueId} not found.`);
  }

  const nextIssue = applyIssuePatch(previousIssue, parsedPatch);
  const nextIssues = issues.map((issue) =>
    issue.id === issueId ? nextIssue : issue,
  );

  writeIssues(nextIssues);

  return {
    issue: nextIssue,
    previousIssue: cloneValue(previousIssue),
  };
}

export async function bulkUpdateIssues(
  issueIds: string[],
  patch: BulkIssuePatch,
): Promise<{ issues: Issue[]; previousIssues: Issue[] }> {
  const parsedPatch = bulkIssuePatchSchema.parse(patch);
  await simulateRequest("write");

  const issues = readIssues();
  const previousIssues = issues.filter((issue) => issueIds.includes(issue.id));
  const nextIssues = applyBulkPatch(issues, issueIds, parsedPatch);

  writeIssues(nextIssues);

  return {
    issues: nextIssues.filter((issue) => issueIds.includes(issue.id)),
    previousIssues: cloneValue(previousIssues),
  };
}

export async function getDashboardSummary(): Promise<DashboardSummary> {
  await simulateRequest("read");
  return createDashboardSummary(readIssues());
}

export async function listSavedViews(): Promise<SavedView[]> {
  await simulateRequest("read");
  return readSavedViews();
}

export async function resetDemoData(): Promise<Issue[]> {
  await waitForLatency(120);
  return resetIssues();
}

export function getDemoRuntimeConfig(): DemoRuntimeConfig {
  return {
    ...defaultDemoRuntimeConfig,
    ...readRuntimeConfig(),
  };
}

