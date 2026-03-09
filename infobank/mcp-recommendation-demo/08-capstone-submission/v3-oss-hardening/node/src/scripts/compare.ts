import { pool } from "../db/client.js";
import {
  listCatalogEntries,
  listEvalCases,
  listExperiments,
  listFeedbackRecords,
  listUsageEvents,
  saveCompareRun
} from "../repositories/catalog-repository.js";
import { runCompare } from "../services/compare-service.js";

async function main() {
  const experimentId = process.argv[2] ?? "exp-release-signal";
  const [catalog, cases, usage, feedback, experiments] = await Promise.all([
    listCatalogEntries(),
    listEvalCases(),
    listUsageEvents(),
    listFeedbackRecords(),
    listExperiments()
  ]);

  const experiment = experiments.find((item) => item.id === experimentId) ?? experiments[0] ?? null;
  const summary = runCompare(cases, catalog, usage, feedback, experiment);
  await saveCompareRun(summary);
  console.log(JSON.stringify(summary, null, 2));
}

await main()
  .catch((error) => {
    console.error(error);
    process.exitCode = 1;
  })
  .finally(async () => {
    await pool.end();
  });
