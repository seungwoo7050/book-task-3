import { pool } from "../db/client.js";
import {
  getInstanceSettings,
  getLatestCompareRun,
  getLatestCompatibilityReport,
  getLatestEvalRun,
  getReleaseCandidateById,
  listReleaseCandidates,
  saveGateReport
} from "../repositories/catalog-repository.js";
import { buildDefaultInstanceSettings } from "../services/instance-service.js";
import { runReleaseGate } from "../services/release-gate-service.js";

async function main() {
  const releaseCandidateId = process.argv[2];
  const candidate = releaseCandidateId
    ? await getReleaseCandidateById(releaseCandidateId)
    : (await listReleaseCandidates())[0] ?? null;

  if (!candidate) {
    throw new Error("No release candidate available");
  }

  const [compatibilityReport, latestEval, latestCompare, settings] = await Promise.all([
    getLatestCompatibilityReport(),
    getLatestEvalRun(),
    getLatestCompareRun(),
    getInstanceSettings()
  ]);

  const report = runReleaseGate(
    candidate,
    compatibilityReport,
    latestEval,
    latestCompare,
    settings ?? buildDefaultInstanceSettings("cli")
  );
  await saveGateReport(report);
  console.log(JSON.stringify(report, null, 2));
}

await main()
  .catch((error) => {
    console.error(error);
    process.exitCode = 1;
  })
  .finally(async () => {
    await pool.end();
  });
