import "reflect-metadata";
import "dotenv/config";

import { createAppDataSource } from "../data-source";

async function run(): Promise<void> {
  const dataSource = createAppDataSource(process.env);
  await dataSource.initialize();
  await dataSource.runMigrations();
  await dataSource.destroy();
}

run().catch((error: unknown) => {
  console.error(error);
  process.exitCode = 1;
});
