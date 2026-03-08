import { pool } from "../db/client.js";
import {
  getLatestCompareRun,
  getLatestCompatibilityReport,
  getLatestEvalRun,
  getReleaseCandidateById,
  listReleaseCandidates,
  saveGateReport
} from "../repositories/catalog-repository.js";
import { runReleaseGate } from "../services/release-gate-service.js";

async function main() {
  const releaseCandidateId = process.argv[2];
  const candidate = releaseCandidateId
    ? await getReleaseCandidateById(releaseCandidateId)
    : (await listReleaseCandidates())[0] ?? null;

  if (!candidate) {
    throw new Error("No release candidate available");
  }

  const [compatibilityReport, latestEval, latestCompare] = await Promise.all([
    getLatestCompatibilityReport(),
    getLatestEvalRun(),
    getLatestCompareRun()
  ]);

  const report = runReleaseGate(candidate, compatibilityReport, latestEval, latestCompare);
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
