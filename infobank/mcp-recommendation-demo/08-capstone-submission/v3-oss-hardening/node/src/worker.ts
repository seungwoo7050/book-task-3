import { startJobWorker, stopBoss } from "./services/job-service.js";

await startJobWorker();

async function shutdown() {
  await stopBoss();
  process.exit(0);
}

process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);
