import { mcpManifestSchema, recommendationRequestSchema } from "@study1-v0/shared";
import cors from "@fastify/cors";
import Fastify from "fastify";
import {
  getCatalogEntryById,
  getLatestEvalRun,
  listCatalogEntries,
  listEvalCases,
  saveEvalRun,
  saveRecommendationRun
} from "./repositories/catalog-repository.js";
import { evaluateOfflineCases } from "./services/eval-service.js";
import { recommendCatalog } from "./services/recommendation-service.js";

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

  app.post("/api/evals/run", async () => {
    const [catalog, cases] = await Promise.all([listCatalogEntries(), listEvalCases()]);
    const summary = evaluateOfflineCases(cases, catalog);
    await saveEvalRun(summary);
    return summary;
  });

  app.get("/api/evals/latest", async () => {
    return { latest: await getLatestEvalRun() };
  });

  return app;
}
