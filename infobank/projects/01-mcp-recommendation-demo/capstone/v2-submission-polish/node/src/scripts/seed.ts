import { catalogSeeds, offlineEvalCases } from "@study1-v0/shared";
import type { UsageEvent } from "@study1-v0/shared";
import { randomUUID } from "node:crypto";
import { db, pool } from "../db/client.js";
import {
  artifactExports,
  catalogEntries,
  compatibilityReports,
  compareRuns,
  evalCases,
  evalRuns,
  experiments,
  feedbackRecords,
  gateReports,
  releaseCandidates,
  recommendationRuns,
  usageEvents
} from "../db/schema.js";

async function main() {
  await db.delete(recommendationRuns);
  await db.delete(evalRuns);
  await db.delete(compareRuns);
  await db.delete(artifactExports);
  await db.delete(gateReports);
  await db.delete(compatibilityReports);
  await db.delete(feedbackRecords);
  await db.delete(usageEvents);
  await db.delete(releaseCandidates);
  await db.delete(experiments);
  await db.delete(evalCases);
  await db.delete(catalogEntries);

  await db.insert(catalogEntries).values(
    catalogSeeds.map((entry) => ({
      id: entry.id,
      slug: entry.slug,
      payload: entry
    }))
  );

  await db.insert(evalCases).values(
    offlineEvalCases.map((item) => ({
      id: item.id,
      payload: item
    }))
  );

  const usageSeed = [
    { catalogId: "release-check-bot", impression: 14, click: 9, accept: 6 },
    { catalogId: "package-registry-guard", impression: 12, click: 6, accept: 3 },
    { catalogId: "korean-docs-search", impression: 11, click: 8, accept: 6 },
    { catalogId: "notion-knowledge-sync", impression: 10, click: 5, accept: 2 }
  ];

  await db.insert(usageEvents).values(
    usageSeed.flatMap((item) => {
      const rows: Array<{ id: string; payload: UsageEvent }> = [];
      for (let index = 0; index < item.impression; index += 1) {
        rows.push({
          id: randomUUID(),
          payload: {
            id: randomUUID(),
            recommendationRunId: "seed-run",
            catalogId: item.catalogId,
            action: "impression",
            actor: "user",
            createdAt: new Date().toISOString(),
            metadata: {}
          }
        });
      }
      for (let index = 0; index < item.click; index += 1) {
        rows.push({
          id: randomUUID(),
          payload: {
            id: randomUUID(),
            recommendationRunId: "seed-run",
            catalogId: item.catalogId,
            action: "click",
            actor: "user",
            createdAt: new Date().toISOString(),
            metadata: {}
          }
        });
      }
      for (let index = 0; index < item.accept; index += 1) {
        rows.push({
          id: randomUUID(),
          payload: {
            id: randomUUID(),
            recommendationRunId: "seed-run",
            catalogId: item.catalogId,
            action: "accept",
            actor: "user",
            createdAt: new Date().toISOString(),
            metadata: {}
          }
        });
      }
      return rows;
    })
  );

  await db.insert(feedbackRecords).values([
    {
      id: randomUUID(),
      payload: {
        id: randomUUID(),
        recommendationRunId: "seed-run",
        catalogId: "release-check-bot",
        scoreDelta: 2,
        noteKo: "릴리즈 시나리오에서 가장 설명이 명확했다.",
        reviewer: "ops-lead",
        createdAt: new Date().toISOString()
      }
    },
    {
      id: randomUUID(),
      payload: {
        id: randomUUID(),
        recommendationRunId: "seed-run",
        catalogId: "korean-docs-search",
        scoreDelta: 2,
        noteKo: "한국어 근거 노출이 좋아서 candidate에서 올릴 가치가 있다.",
        reviewer: "search-owner",
        createdAt: new Date().toISOString()
      }
    },
    {
      id: randomUUID(),
      payload: {
        id: randomUUID(),
        recommendationRunId: "seed-run",
        catalogId: "package-registry-guard",
        scoreDelta: 1,
        noteKo: "호환성 점검은 좋지만 릴리즈 체크 전체 맥락은 부족하다.",
        reviewer: "release-manager",
        createdAt: new Date().toISOString()
      }
    }
  ]);

  await db.insert(experiments).values([
    {
      id: "exp-release-signal",
      payload: {
        id: "exp-release-signal",
        name: "release-signal-rerank",
        baselineStrategy: "weighted-baseline-v0",
        candidateStrategy: "signal-rerank-v1",
        trafficSplitPercent: 50,
        status: "running",
        hypothesisKo: "실사용 CTR과 operator feedback을 넣으면 릴리즈/문서 질의의 top1 정렬이 개선된다."
      }
    }
  ]);

  const now = new Date().toISOString();
  await db.insert(releaseCandidates).values([
    {
      id: "rc-release-check-bot-1-5-0",
      payload: {
        id: "rc-release-check-bot-1-5-0",
        name: "release-check-bot v1.5.0",
        manifestId: "release-check-bot",
        previousVersion: "1.4.0",
        releaseVersion: "1.5.0",
        targetClientVersion: "1.2.0",
        releaseNotesKo:
          "변경 요약: changeset 상태와 호환성 체크를 한 번에 보여주는 dry-run 흐름을 정리했습니다.\n검증: offline eval, compare run, compatibility gate, release gate를 모두 재실행했습니다.\n리스크: tested client version 밖의 런타임은 별도 검증이 필요합니다.",
        requiredDocs: [
          "docs/README.md",
          "docs/runbook.md",
          "docs/eval-proof.md",
          "docs/compare-report.md",
          "docs/compatibility-report.md",
          "docs/release-gate-proof.md",
          "docs/korean-market-fit.md"
        ],
        requiredArtifacts: [
          ".changeset/config.json",
          ".changeset/mcp-v2-demo.md",
          "../../../../.github/workflows/mcp-v2-dry-run.yml"
        ],
        deprecatedFieldsUsed: [],
        owner: "release-ops",
        status: "candidate",
        createdAt: now,
        updatedAt: now
      }
    }
  ]);

  console.log(
    `Seeded ${catalogSeeds.length} catalog entries, ${offlineEvalCases.length} eval cases, usage signals, feedback, experiments, and release candidates.`
  );
}

await main()
  .catch((error) => {
    console.error(error);
    process.exitCode = 1;
  })
  .finally(async () => {
    await pool.end();
  });
