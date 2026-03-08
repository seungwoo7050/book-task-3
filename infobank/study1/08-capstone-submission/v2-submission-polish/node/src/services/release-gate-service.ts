import type { CompatibilityReport, ReleaseCandidate, ReleaseGateReport } from "@study1-v0/shared";
import { randomUUID } from "node:crypto";
import { existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

type EvalSummary = {
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
} | null;

type CompareSummary = {
  metrics: {
    baselineNdcg3: number;
    candidateNdcg3: number;
    uplift: number;
    baselineTop1HitRate: number;
    candidateTop1HitRate: number;
  };
} | null;

const workspaceRoot = path.resolve(fileURLToPath(new URL("../../..", import.meta.url)));

function requiredPathsExist(paths: string[]) {
  return paths.every((relativePath) => existsSync(path.resolve(workspaceRoot, relativePath)));
}

function releaseNotesComplete(notes: string) {
  return ["변경 요약", "검증", "리스크"].every((section) => notes.includes(section));
}

export function runReleaseGate(
  candidate: ReleaseCandidate,
  compatibilityReport: CompatibilityReport | null,
  latestEval: EvalSummary,
  latestCompare: CompareSummary
): ReleaseGateReport {
  const top3Recall = latestEval?.metrics.top3Recall ?? 0;
  const explanationCompleteness = latestEval?.metrics.explanationCompleteness ?? 0;
  const forbiddenHitRate = latestEval?.metrics.forbiddenHitRate ?? 1;
  const baselineNdcg3 = latestCompare?.metrics.baselineNdcg3 ?? 0;
  const candidateNdcg3 = latestCompare?.metrics.candidateNdcg3 ?? 0;
  const uplift = latestCompare?.metrics.uplift ?? -1;

  const reasons: string[] = [];

  if (!compatibilityReport?.passed) {
    reasons.push("compatibility gate가 통과하지 않았습니다.");
  }

  if (!(latestEval?.acceptance.top3RecallPass && latestEval.acceptance.explanationPass && latestEval.acceptance.forbiddenPass)) {
    reasons.push("offline eval acceptance 기준(top3 recall, explanation completeness, forbidden hit)을 만족하지 못했습니다.");
  }

  if (!(candidateNdcg3 >= baselineNdcg3 && uplift >= 0.02)) {
    reasons.push("candidate compare uplift가 임계값 0.02를 넘지 못했거나 baseline보다 낮습니다.");
  }

  if (!requiredPathsExist(candidate.requiredDocs) || !requiredPathsExist(candidate.requiredArtifacts)) {
    reasons.push("제출용 docs 또는 artifact 파일이 누락되었습니다.");
  }

  if (!releaseNotesComplete(candidate.releaseNotesKo)) {
    reasons.push("release note에 '변경 요약', '검증', '리스크' 섹션이 모두 들어 있지 않습니다.");
  }

  return {
    id: randomUUID(),
    releaseCandidateId: candidate.id,
    passed: reasons.length === 0,
    reasons,
    metrics: {
      top3Recall,
      explanationCompleteness,
      forbiddenHitRate,
      baselineNdcg3,
      candidateNdcg3,
      uplift
    },
    checkedAt: new Date().toISOString()
  };
}
