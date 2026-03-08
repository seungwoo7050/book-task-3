import type { CatalogEntry, CompatibilityReport, ReleaseCandidate } from "@study1-v0/shared";
import { mcpManifestSchema } from "@study1-v0/shared";
import { randomUUID } from "node:crypto";
import semver from "semver";

type CompatibilityCheck = CompatibilityReport["checks"][number];

function buildCheck(name: string, passed: boolean, detailKo: string): CompatibilityCheck {
  return { name, passed, detailKo };
}

export function runCompatibilityGate(
  candidate: ReleaseCandidate,
  entry: CatalogEntry
): CompatibilityReport {
  const manifestValidation = mcpManifestSchema.safeParse(entry);
  const runtimeRange = `>=${entry.compatibility.minimumClientVersion} <=${entry.compatibility.maximumClientVersion}`;
  const runtimeSupported =
    semver.valid(candidate.targetClientVersion) !== null &&
    semver.satisfies(candidate.targetClientVersion, runtimeRange) &&
    entry.compatibility.testedClientVersions.includes(candidate.targetClientVersion);

  const previousMajor = semver.valid(candidate.previousVersion)
    ? semver.major(candidate.previousVersion)
    : null;
  const releaseMajor = semver.valid(candidate.releaseVersion)
    ? semver.major(candidate.releaseVersion)
    : null;
  const breakingChangeCount = entry.compatibility.breakingChanges.length;
  const semverConsistency =
    previousMajor !== null &&
    releaseMajor !== null &&
    ((releaseMajor > previousMajor && breakingChangeCount > 0) ||
      (releaseMajor === previousMajor && breakingChangeCount === 0));

  const deprecatedFieldsClear = candidate.deprecatedFieldsUsed.length === 0;
  const koreanMetadataComplete =
    entry.summaryKo.length >= 10 &&
    entry.descriptionKo.length >= 20 &&
    entry.koreanUseCases.length >= 2 &&
    entry.differentiationPoints.length >= 2 &&
    entry.exposure.userFacingSummaryKo.length >= 10;

  const checks = [
    buildCheck(
      "manifest-schema",
      manifestValidation.success && candidate.releaseVersion === entry.version,
      manifestValidation.success
        ? `manifest schema가 유효하며 release version ${candidate.releaseVersion}이 manifest와 일치합니다.`
        : "manifest schema 검증이 실패했습니다."
    ),
    buildCheck(
      "runtime-range",
      runtimeSupported,
      runtimeSupported
        ? `target client ${candidate.targetClientVersion}이 허용 범위 ${runtimeRange} 및 tested set에 포함됩니다.`
        : `target client ${candidate.targetClientVersion}이 허용 범위 ${runtimeRange} 또는 tested set과 맞지 않습니다.`
    ),
    buildCheck(
      "semver-consistency",
      semverConsistency,
      semverConsistency
        ? "semver bump와 breaking change 메타데이터가 일관됩니다."
        : "major/minor bump와 breaking change 메타데이터가 일치하지 않습니다."
    ),
    buildCheck(
      "deprecated-fields",
      deprecatedFieldsClear,
      deprecatedFieldsClear
        ? "deprecated field 사용이 없습니다."
        : `deprecated field 사용이 감지되었습니다: ${candidate.deprecatedFieldsUsed.join(", ")}`
    ),
    buildCheck(
      "korean-metadata",
      koreanMetadataComplete,
      koreanMetadataComplete
        ? "한국어 설명, use case, differentiation 메타데이터가 모두 채워져 있습니다."
        : "한국어 메타데이터가 일부 비어 있습니다."
    )
  ];

  return {
    id: randomUUID(),
    releaseCandidateId: candidate.id,
    candidateVersion: candidate.releaseVersion,
    passed: checks.every((item) => item.passed),
    checks,
    issues: checks.filter((item) => !item.passed).map((item) => item.detailKo),
    checkedAt: new Date().toISOString()
  };
}
