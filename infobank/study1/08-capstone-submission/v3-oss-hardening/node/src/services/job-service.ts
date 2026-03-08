import type { JobName, JobRun, StoredUser } from "@study1-v3/shared";
import PgBoss from "pg-boss";
import { config } from "../config.js";
import {
  createAuditEvent,
  createJobRun,
  getCatalogEntryById,
  getInstanceSettings,
  getJobRunById,
  getLatestArtifactExport,
  getLatestCompareRun,
  getLatestCompatibilityReport,
  getLatestEvalRun,
  getLatestGateReport,
  getReleaseCandidateById,
  listCatalogEntries,
  listEvalCases,
  listExperiments,
  listFeedbackRecords,
  listUsageEvents,
  saveArtifactExport,
  saveCompareRun,
  saveCompatibilityReport,
  saveEvalRun,
  saveGateReport,
  updateJobRun
} from "../repositories/catalog-repository.js";
import { buildAuditEvent } from "./audit-service.js";
import { buildSubmissionArtifact } from "./artifact-service.js";
import { runCompare } from "./compare-service.js";
import { runCompatibilityGate } from "./compatibility-service.js";
import { evaluateOfflineCases } from "./eval-service.js";
import { buildDefaultInstanceSettings } from "./instance-service.js";
import { runReleaseGate } from "./release-gate-service.js";

type EvalPayload = Record<string, never>;
type ComparePayload = { experimentId?: string | null };
type ReleasePayload = { releaseCandidateId?: string | null };

type QueuePayload = EvalPayload | ComparePayload | ReleasePayload;
const jobQueues = [
  "eval",
  "compare",
  "compatibility",
  "release-gate",
  "artifact-export"
] satisfies JobName[];

let bossPromise: Promise<PgBoss> | null = null;
let workerStarted = false;

async function ensureJobQueues(boss: PgBoss) {
  for (const queueName of jobQueues) {
    await boss.createQueue(queueName);
  }
}

function buildJobSummary(name: JobName, status: JobRun["status"], output: Record<string, unknown> | null) {
  if (status === "failed") {
    return `${name} 작업이 실패했습니다.`;
  }

  switch (name) {
    case "eval":
      return `offline eval이 완료됐고 top3 recall ${(Number(output?.top3Recall ?? 0) * 100).toFixed(1)}%를 기록했습니다.`;
    case "compare":
      return `compare snapshot이 완료됐고 uplift ${Number(output?.uplift ?? 0).toFixed(3)}를 기록했습니다.`;
    case "compatibility":
      return `compatibility gate가 ${output?.passed ? "PASS" : "FAIL"}로 완료됐습니다.`;
    case "release-gate":
      return `release gate가 ${output?.passed ? "PASS" : "FAIL"}로 완료됐습니다.`;
    case "artifact-export":
      return "submission artifact export가 완료됐습니다.";
    default:
      return `${name} 작업이 완료됐습니다.`;
  }
}

async function performJob(name: JobName, payload: QueuePayload) {
  switch (name) {
    case "eval": {
      const [catalog, cases] = await Promise.all([listCatalogEntries(), listEvalCases()]);
      const summary = evaluateOfflineCases(cases, catalog);
      await saveEvalRun(summary);
      return {
        output: {
          reportId: summary.id,
          top3Recall: summary.metrics.top3Recall,
          explanationCompleteness: summary.metrics.explanationCompleteness,
          forbiddenHitRate: summary.metrics.forbiddenHitRate
        },
        detailKo: "offline eval이 완료되었습니다."
      };
    }
    case "compare": {
      const [catalog, cases, usage, feedback, experiments] = await Promise.all([
        listCatalogEntries(),
        listEvalCases(),
        listUsageEvents(),
        listFeedbackRecords(),
        listExperiments()
      ]);
      const experiment =
        experiments.find((item) => item.id === ((payload as ComparePayload).experimentId ?? "")) ??
        experiments[0] ??
        null;
      const summary = runCompare(cases, catalog, usage, feedback, experiment);
      await saveCompareRun(summary);
      return {
        output: {
          reportId: summary.id,
          baselineNdcg3: summary.metrics.baselineNdcg3,
          candidateNdcg3: summary.metrics.candidateNdcg3,
          uplift: summary.metrics.uplift
        },
        detailKo: "compare snapshot이 완료되었습니다."
      };
    }
    case "compatibility": {
      const releaseCandidate =
        ((payload as ReleasePayload).releaseCandidateId
          ? await getReleaseCandidateById((payload as ReleasePayload).releaseCandidateId!)
          : null) ??
        (await getReleaseCandidateById("rc-release-check-bot-1-5-0"));
      if (!releaseCandidate) {
        throw new Error("릴리즈 후보를 찾지 못했습니다.");
      }
      const entry = await getCatalogEntryById(releaseCandidate.manifestId);
      if (!entry) {
        throw new Error(`Catalog entry ${releaseCandidate.manifestId} not found`);
      }
      const report = runCompatibilityGate(releaseCandidate, entry);
      await saveCompatibilityReport(report);
      return {
        output: {
          reportId: report.id,
          passed: report.passed,
          releaseCandidateId: releaseCandidate.id
        },
        detailKo: "compatibility gate가 완료되었습니다."
      };
    }
    case "release-gate": {
      const releaseCandidate =
        ((payload as ReleasePayload).releaseCandidateId
          ? await getReleaseCandidateById((payload as ReleasePayload).releaseCandidateId!)
          : null) ??
        (await getReleaseCandidateById("rc-release-check-bot-1-5-0"));
      if (!releaseCandidate) {
        throw new Error("릴리즈 후보를 찾지 못했습니다.");
      }
      const [compatibilityReport, latestEval, latestCompare, settings] = await Promise.all([
        getLatestCompatibilityReport(),
        getLatestEvalRun(),
        getLatestCompareRun(),
        getInstanceSettings()
      ]);
      const report = runReleaseGate(
        releaseCandidate,
        compatibilityReport,
        latestEval,
        latestCompare,
        settings ?? buildDefaultInstanceSettings("system")
      );
      await saveGateReport(report);
      return {
        output: {
          reportId: report.id,
          passed: report.passed,
          uplift: report.metrics.uplift,
          releaseCandidateId: releaseCandidate.id
        },
        detailKo: "release gate가 완료되었습니다."
      };
    }
    case "artifact-export": {
      const releaseCandidate =
        ((payload as ReleasePayload).releaseCandidateId
          ? await getReleaseCandidateById((payload as ReleasePayload).releaseCandidateId!)
          : null) ??
        (await getReleaseCandidateById("rc-release-check-bot-1-5-0"));
      if (!releaseCandidate) {
        throw new Error("릴리즈 후보를 찾지 못했습니다.");
      }
      const [compatibilityReport, gateReport, latestEval, latestCompare, latestArtifact] =
        await Promise.all([
          getLatestCompatibilityReport(),
          getLatestGateReport(),
          getLatestEvalRun(),
          getLatestCompareRun(),
          getLatestArtifactExport()
        ]);
      const artifact = buildSubmissionArtifact(
        releaseCandidate,
        compatibilityReport,
        gateReport,
        latestEval,
        latestCompare
      );
      await saveArtifactExport(artifact);
      return {
        output: {
          artifactId: artifact.id,
          releaseCandidateId: releaseCandidate.id,
          previousArtifactId: latestArtifact?.id ?? null
        },
        detailKo: "submission artifact export가 완료되었습니다."
      };
    }
    default:
      throw new Error(`Unsupported job ${String(name)}`);
  }
}

export async function getBoss() {
  if (!bossPromise) {
    bossPromise = (async () => {
      const boss = new PgBoss(config.databaseUrl);
      await boss.start();
      await ensureJobQueues(boss);
      return boss;
    })();
  }

  return bossPromise;
}

export async function stopBoss() {
  if (!bossPromise) return;
  const boss = await bossPromise;
  await boss.stop();
  bossPromise = null;
  workerStarted = false;
}

export async function enqueueJob(name: JobName, payload: QueuePayload, actor: StoredUser) {
  const boss = await getBoss();
  const jobId = await boss.send(name, payload);
  if (!jobId) {
    throw new Error(`Failed to enqueue ${name} job`);
  }
  const run: JobRun = {
    id: jobId,
    name,
    status: "pending",
    createdByUserId: actor.id,
    createdByEmail: actor.email,
    payload: payload as Record<string, unknown>,
    resultSummaryKo: null,
    errorSummary: null,
    output: null,
    createdAt: new Date().toISOString(),
    startedAt: null,
    finishedAt: null
  };

  await createJobRun(run);
  await createAuditEvent(
    buildAuditEvent({
      actor,
      action: "job.enqueue",
      targetType: "job",
      targetId: jobId,
      detailKo: `${name} 작업이 큐에 등록됐습니다.`,
      metadata: { name, payload }
    })
  );

  return { jobId, status: run.status };
}

async function markJobRunning(jobId: string) {
  const current = await getJobRunById(jobId);
  if (!current) return;
  await updateJobRun({
    ...current,
    status: "running",
    startedAt: new Date().toISOString()
  });
}

async function markJobCompleted(jobId: string, name: JobName, output: Record<string, unknown>) {
  const current = await getJobRunById(jobId);
  if (!current) return;
  await updateJobRun({
    ...current,
    status: "completed",
    output,
    resultSummaryKo: buildJobSummary(name, "completed", output),
    errorSummary: null,
    finishedAt: new Date().toISOString()
  });
}

async function markJobFailed(jobId: string, name: JobName, error: Error) {
  const current = await getJobRunById(jobId);
  if (!current) return;
  await updateJobRun({
    ...current,
    status: "failed",
    output: null,
    resultSummaryKo: buildJobSummary(name, "failed", null),
    errorSummary: error.message,
    finishedAt: new Date().toISOString()
  });
}

export async function startJobWorker() {
  if (workerStarted) {
    return;
  }

  const boss = await getBoss();
  workerStarted = true;

  for (const queueName of jobQueues) {
    await boss.work(queueName, async (jobs) => {
      for (const job of Array.isArray(jobs) ? jobs : [jobs]) {
        await markJobRunning(job.id);

        try {
          const result = await performJob(queueName, (job.data ?? {}) as QueuePayload);
          await markJobCompleted(job.id, queueName, result.output);
        } catch (error) {
          const normalized = error instanceof Error ? error : new Error(String(error));
          await markJobFailed(job.id, queueName, normalized);
          throw normalized;
        }
      }
    });
  }
}
