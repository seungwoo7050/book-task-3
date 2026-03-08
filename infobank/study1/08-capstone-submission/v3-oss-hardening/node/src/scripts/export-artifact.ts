import { pool } from "../db/client.js";
import {
  getLatestCompareRun,
  getLatestCompatibilityReport,
  getLatestEvalRun,
  getLatestGateReport,
  getReleaseCandidateById,
  listReleaseCandidates,
  saveArtifactExport
} from "../repositories/catalog-repository.js";
import { buildSubmissionArtifact } from "../services/artifact-service.js";

async function main() {
  const releaseCandidateId = process.argv[2];
  const candidate = releaseCandidateId
    ? await getReleaseCandidateById(releaseCandidateId)
    : (await listReleaseCandidates())[0] ?? null;

  if (!candidate) {
    throw new Error("No release candidate available");
  }

  const [compatibilityReport, gateReport, latestEval, latestCompare] = await Promise.all([
    getLatestCompatibilityReport(),
    getLatestGateReport(),
    getLatestEvalRun(),
    getLatestCompareRun()
  ]);

  const artifact = buildSubmissionArtifact(
    candidate,
    compatibilityReport,
    gateReport,
    latestEval,
    latestCompare
  );
  await saveArtifactExport(artifact);
  console.log(artifact.content);
}

await main()
  .catch((error) => {
    console.error(error);
    process.exitCode = 1;
  })
  .finally(async () => {
    await pool.end();
  });
