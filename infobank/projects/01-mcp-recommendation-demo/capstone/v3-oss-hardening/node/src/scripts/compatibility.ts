import { pool } from "../db/client.js";
import {
  getCatalogEntryById,
  getReleaseCandidateById,
  listReleaseCandidates,
  saveCompatibilityReport
} from "../repositories/catalog-repository.js";
import { runCompatibilityGate } from "../services/compatibility-service.js";

async function main() {
  const releaseCandidateId = process.argv[2];
  const candidate = releaseCandidateId
    ? await getReleaseCandidateById(releaseCandidateId)
    : (await listReleaseCandidates())[0] ?? null;

  if (!candidate) {
    throw new Error("No release candidate available");
  }

  const entry = await getCatalogEntryById(candidate.manifestId);
  if (!entry) {
    throw new Error(`Catalog entry ${candidate.manifestId} not found`);
  }

  const report = runCompatibilityGate(candidate, entry);
  await saveCompatibilityReport(report);
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
