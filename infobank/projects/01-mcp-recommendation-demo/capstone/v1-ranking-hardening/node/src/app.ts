import {
  catalogEntrySchema,
  experimentConfigSchema,
  feedbackRecordSchema,
  mcpManifestSchema,
  recommendationRequestSchema,
  usageEventSchema
} from "@study1-v0/shared";
import cors from "@fastify/cors";
import Fastify from "fastify";
import {
  createCatalogEntry,
  createExperiment,
  createFeedbackRecord,
  createUsageEvent,
  deleteCatalogEntry,
  deleteExperiment,
  getCatalogEntryById,
  getLatestCompareRun,
  getLatestEvalRun,
  listCatalogEntries,
  listEvalCases,
  listExperiments,
  listFeedbackRecords,
  listUsageEvents,
  saveEvalRun,
  saveRecommendationRun,
  saveCompareRun,
  updateCatalogEntry,
  updateExperiment
} from "./repositories/catalog-repository.js";
import { runCompare } from "./services/compare-service.js";
import { evaluateOfflineCases } from "./services/eval-service.js";
import { recommendCatalog } from "./services/recommendation-service.js";
import { rerankCatalog } from "./services/rerank-service.js";

export async function buildApp() {
  const app = Fastify();
  await app.register(cors, { origin: true });

  app.get("/healthz", async () => ({ status: "ok" }));

  app.get("/api/catalog", async () => {
    const items = await listCatalogEntries();
    return { items };
  });

  app.get("/api/catalog/:id", async (request, reply) => {
    const params = request.params as { id: string };
    const item = await getCatalogEntryById(params.id);

    if (!item) {
      reply.code(404);
      return { message: "Catalog entry not found" };
    }

    return { item };
  });

  app.post("/api/manifests/validate", async (request) => {
    const parsed = mcpManifestSchema.safeParse(request.body);
    return parsed.success
      ? { valid: true, issues: [], manifest: parsed.data }
      : {
          valid: false,
          issues: parsed.error.issues.map((issue) => `${issue.path.join(".")}: ${issue.message}`)
        };
  });

  app.post("/api/recommendations", async (request) => {
    const parsed = recommendationRequestSchema.parse(request.body);
    const catalog = await listCatalogEntries();
    const result = recommendCatalog(parsed, catalog);
    await saveRecommendationRun(result);
    return result;
  });

  app.post("/api/recommendations/candidate", async (request) => {
    const parsed = recommendationRequestSchema.parse(request.body);
    const [catalog, usage, feedback] = await Promise.all([
      listCatalogEntries(),
      listUsageEvents(),
      listFeedbackRecords()
    ]);
    const result = rerankCatalog(parsed, catalog, usage, feedback);
    await saveRecommendationRun(result);
    return result;
  });

  app.post("/api/evals/run", async () => {
    const [catalog, cases] = await Promise.all([listCatalogEntries(), listEvalCases()]);
    const summary = evaluateOfflineCases(cases, catalog);
    await saveEvalRun(summary);
    return summary;
  });

  app.get("/api/evals/latest", async () => {
    return { latest: await getLatestEvalRun() };
  });

  app.post("/api/usage-events", async (request) => {
    const event = usageEventSchema.parse(request.body);
    await createUsageEvent(event);
    return { saved: true };
  });

  app.get("/api/usage-events", async () => {
    const items = await listUsageEvents();
    const totals = items.reduce(
      (accumulator, item) => {
        accumulator[item.action] += 1;
        return accumulator;
      },
      { impression: 0, click: 0, accept: 0, dismiss: 0 }
    );

    return { items, totals };
  });

  app.post("/api/feedback", async (request) => {
    const record = feedbackRecordSchema.parse(request.body);
    await createFeedbackRecord(record);
    return { saved: true };
  });

  app.get("/api/feedback", async () => {
    return { items: await listFeedbackRecords() };
  });

  app.get("/api/experiments", async () => {
    return { items: await listExperiments() };
  });

  app.post("/api/experiments", async (request) => {
    const experiment = experimentConfigSchema.parse(request.body);
    await createExperiment(experiment);
    return { saved: true };
  });

  app.put("/api/experiments/:id", async (request) => {
    const experiment = experimentConfigSchema.parse({
      ...(request.body as object),
      id: (request.params as { id: string }).id
    });
    await updateExperiment(experiment);
    return { saved: true };
  });

  app.delete("/api/experiments/:id", async (request) => {
    await deleteExperiment((request.params as { id: string }).id);
    return { deleted: true };
  });

  app.post("/api/catalog", async (request) => {
    const catalogEntry = catalogEntrySchema.parse(request.body);
    await createCatalogEntry(catalogEntry);
    return { saved: true };
  });

  app.put("/api/catalog/:id", async (request) => {
    const catalogEntry = catalogEntrySchema.parse({
      ...(request.body as Parameters<typeof createCatalogEntry>[0]),
      id: (request.params as { id: string }).id
    });
    await updateCatalogEntry(catalogEntry);
    return { saved: true };
  });

  app.delete("/api/catalog/:id", async (request) => {
    await deleteCatalogEntry((request.params as { id: string }).id);
    return { deleted: true };
  });

  app.post("/api/compare/run", async (request) => {
    const experimentId = (request.body as { experimentId?: string } | undefined)?.experimentId;
    const [catalog, cases, usage, feedback, experiments] = await Promise.all([
      listCatalogEntries(),
      listEvalCases(),
      listUsageEvents(),
      listFeedbackRecords(),
      listExperiments()
    ]);
    const experiment = experiments.find((item) => item.id === experimentId) ?? null;
    const summary = runCompare(cases, catalog, usage, feedback, experiment);
    await saveCompareRun(summary);
    return summary;
  });

  app.get("/api/compare/latest", async () => {
    return { latest: await getLatestCompareRun() };
  });

  return app;
}
