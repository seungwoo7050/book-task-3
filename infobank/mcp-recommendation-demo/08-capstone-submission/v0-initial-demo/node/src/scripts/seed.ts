import { catalogSeeds, offlineEvalCases } from "@study1-v0/shared";
import { db, pool } from "../db/client.js";
import { catalogEntries, evalCases, evalRuns, recommendationRuns } from "../db/schema.js";

async function main() {
  await db.delete(recommendationRuns);
  await db.delete(evalRuns);
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

  console.log(`Seeded ${catalogSeeds.length} catalog entries and ${offlineEvalCases.length} eval cases.`);
}

await main()
  .catch((error) => {
    console.error(error);
    process.exitCode = 1;
  })
  .finally(async () => {
    await pool.end();
  });
