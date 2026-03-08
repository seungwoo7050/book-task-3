import { listCatalogEntries, listEvalCases, saveEvalRun } from "../repositories/catalog-repository.js";
import { pool } from "../db/client.js";
import { evaluateOfflineCases } from "../services/eval-service.js";

async function main() {
  const [catalog, cases] = await Promise.all([listCatalogEntries(), listEvalCases()]);
  const summary = evaluateOfflineCases(cases, catalog);
  await saveEvalRun(summary);
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
