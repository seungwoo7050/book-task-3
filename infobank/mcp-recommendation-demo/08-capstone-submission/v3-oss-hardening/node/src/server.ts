import { buildApp } from "./app.js";
import { config } from "./config.js";
import { startJobWorker } from "./services/job-service.js";

const app = await buildApp();

if (config.inlineJobWorker) {
  await startJobWorker();
}

await app.listen({
  port: config.port,
  host: "0.0.0.0"
});
