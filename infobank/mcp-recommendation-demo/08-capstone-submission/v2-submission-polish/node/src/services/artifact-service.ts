import type {
  ArtifactExport,
  CompatibilityReport,
  ReleaseCandidate,
  ReleaseGateReport
} from "@study1-v0/shared";
import { randomUUID } from "node:crypto";

type EvalSummary = {
  metrics: {
    top3Recall: number;
    explanationCompleteness: number;
    forbiddenHitRate: number;
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

export function buildSubmissionArtifact(
  candidate: ReleaseCandidate,
  compatibilityReport: CompatibilityReport | null,
  gateReport: ReleaseGateReport | null,
  latestEval: EvalSummary,
  latestCompare: CompareSummary
): ArtifactExport {
  const content = [
    `# ${candidate.name}`,
    "",
    `- release candidate id: ${candidate.id}`,
    `- manifest id: ${candidate.manifestId}`,
    `- version: ${candidate.releaseVersion}`,
    `- target client: ${candidate.targetClientVersion}`,
    `- owner: ${candidate.owner}`,
    `- compatibility passed: ${compatibilityReport?.passed ?? false}`,
    `- release gate passed: ${gateReport?.passed ?? false}`,
    "",
    "## Release Notes",
    candidate.releaseNotesKo,
    "",
    "## Offline Eval",
    `- top3 recall: ${(latestEval?.metrics.top3Recall ?? 0).toFixed(3)}`,
    `- explanation completeness: ${(latestEval?.metrics.explanationCompleteness ?? 0).toFixed(3)}`,
    `- forbidden hit rate: ${(latestEval?.metrics.forbiddenHitRate ?? 0).toFixed(3)}`,
    "",
    "## Compare Snapshot",
    `- baseline nDCG@3: ${(latestCompare?.metrics.baselineNdcg3 ?? 0).toFixed(3)}`,
    `- candidate nDCG@3: ${(latestCompare?.metrics.candidateNdcg3 ?? 0).toFixed(3)}`,
    `- uplift: ${(latestCompare?.metrics.uplift ?? 0).toFixed(3)}`,
    "",
    "## Compatibility Issues",
    ...(compatibilityReport?.issues.length
      ? compatibilityReport.issues.map((item) => `- ${item}`)
      : ["- none"]),
    "",
    "## Release Gate Reasons",
    ...(gateReport?.reasons.length ? gateReport.reasons.map((item) => `- ${item}`) : ["- none"])
  ].join("\n");

  return {
    id: randomUUID(),
    releaseCandidateId: candidate.id,
    format: "markdown",
    content,
    createdAt: new Date().toISOString()
  };
}
