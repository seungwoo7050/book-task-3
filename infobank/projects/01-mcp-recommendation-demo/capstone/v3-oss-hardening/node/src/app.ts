import {
  artifactExportSchema,
  authLoginRequestSchema,
  authSessionResponseSchema,
  catalogEntrySchema,
  catalogImportBundleSchema,
  compatibilityReportSchema,
  createUserRequestSchema,
  experimentConfigSchema,
  feedbackRecordSchema,
  jobEnqueueResponseSchema,
  jobNameSchema,
  jobRunSchema,
  mcpManifestSchema,
  publicUserSchema,
  recommendationRequestSchema,
  releaseCandidateSchema,
  releaseGateReportSchema,
  updateSettingsRequestSchema,
  updateUserRequestSchema,
  usageEventSchema,
  type InstanceSettings,
  type StoredUser,
  type User
} from "@study1-v3/shared";
import cookie from "@fastify/cookie";
import cors from "@fastify/cors";
import Fastify from "fastify";
import { randomUUID } from "node:crypto";
import { config } from "./config.js";
import {
  createAuditEvent,
  createCatalogEntry,
  createExperiment,
  createFeedbackRecord,
  createReleaseCandidate,
  createUsageEvent,
  deleteCatalogEntry,
  deleteExperiment,
  deleteReleaseCandidate,
  deleteSessionById,
  exportCatalogImportBundle,
  getCatalogEntryById,
  getInstanceSettings,
  getJobRunById,
  getLatestArtifactExport,
  getLatestCompareRun,
  getLatestCompatibilityReport,
  getLatestEvalRun,
  getLatestGateReport,
  getReleaseCandidateById,
  getSessionRecordByTokenHash,
  getStoredUserByEmail,
  getStoredUserById,
  listAuditEvents,
  listCatalogEntries,
  listExperiments,
  listFeedbackRecords,
  listRecentJobRuns,
  listReleaseCandidates,
  listUsageEvents,
  listUsers,
  purgeExpiredSessions,
  saveInstanceSettings,
  saveRecommendationRun,
  saveStoredUser,
  touchSession,
  updateCatalogEntry,
  updateExperiment,
  updateReleaseCandidate,
  upsertCatalogImportBundle
} from "./repositories/catalog-repository.js";
import { buildAuditEvent } from "./services/audit-service.js";
import {
  SESSION_COOKIE_NAME,
  buildStoredUser,
  hashPassword,
  hashSessionToken,
  issueSession,
  refreshSession,
  toPublicUser,
  verifyPassword
} from "./services/auth-service.js";
import { buildDefaultInstanceSettings } from "./services/instance-service.js";
import { enqueueJob } from "./services/job-service.js";
import { recommendCatalog } from "./services/recommendation-service.js";
import { rerankCatalog } from "./services/rerank-service.js";
import { createSessionRecord } from "./repositories/catalog-repository.js";

const sessionCookieOptions = {
  path: "/",
  httpOnly: true,
  sameSite: "lax" as const,
  secure: false
};

type AuthContext = {
  user: StoredUser;
  settings: InstanceSettings;
};

async function ensureSettings() {
  const current = await getInstanceSettings();
  if (current) {
    return current;
  }

  const settings = buildDefaultInstanceSettings("system-bootstrap");
  await saveInstanceSettings(settings);
  return settings;
}

export async function buildApp() {
  const app = Fastify();
  await app.register(cookie, { secret: config.sessionSecret });
  await app.register(cors, {
    origin: config.appBaseUrl,
    credentials: true
  });

  await ensureSettings();

  async function resolveAuth(
    request: { cookies: Record<string, string | undefined> },
    reply: {
      code: (code: number) => typeof reply;
      setCookie: (name: string, value: string, options: Record<string, unknown>) => void;
      clearCookie: (name: string, options: Record<string, unknown>) => void;
    },
    roles?: Array<User["role"]>
  ): Promise<AuthContext | null> {
    await purgeExpiredSessions();
    const token = request.cookies[SESSION_COOKIE_NAME];

    if (!token) {
      reply.code(401);
      return null;
    }

    const record = await getSessionRecordByTokenHash(hashSessionToken(token));
    if (!record) {
      reply.clearCookie(SESSION_COOKIE_NAME, sessionCookieOptions);
      reply.code(401);
      return null;
    }

    const session = refreshSession(record.payload);
    const user = await getStoredUserById(session.userId);

    if (!user || !user.isActive) {
      await deleteSessionById(record.id);
      reply.clearCookie(SESSION_COOKIE_NAME, sessionCookieOptions);
      reply.code(401);
      return null;
    }

    if (roles && !roles.includes(user.role)) {
      reply.code(403);
      return null;
    }

    await touchSession(session);
    reply.setCookie(SESSION_COOKIE_NAME, token, {
      ...sessionCookieOptions,
      expires: new Date(session.expiresAt)
    });

    const settings = (await getInstanceSettings()) ?? buildDefaultInstanceSettings("system-bootstrap");
    return {
      user,
      settings
    };
  }

  app.get("/healthz", async () => ({ status: "ok" }));

  app.get("/readyz", async () => {
    const settings = await ensureSettings();
    return {
      status: "ready",
      workspaceName: settings.workspaceName
    };
  });

  app.get("/metrics", async (_request, reply) => {
    const [usersList, jobs] = await Promise.all([listUsers(), listRecentJobRuns()]);
    const statusCounts = jobs.reduce<Record<string, number>>((acc, job) => {
      acc[job.status] = (acc[job.status] ?? 0) + 1;
      return acc;
    }, {});

    reply.header("content-type", "text/plain; version=0.0.4");
    return [
      "# HELP study1_users_total Total users in the instance",
      "# TYPE study1_users_total gauge",
      `study1_users_total ${usersList.length}`,
      "# HELP study1_job_runs_total Recent job runs by status",
      "# TYPE study1_job_runs_total gauge",
      ...Object.entries(statusCounts).map(
        ([status, count]) => `study1_job_runs_total{status="${status}"} ${count}`
      )
    ].join("\n");
  });

  app.post("/api/auth/login", async (request, reply) => {
    const body = authLoginRequestSchema.parse(request.body);
    const user = await getStoredUserByEmail(body.email);

    if (!user || !user.isActive || !(await verifyPassword(user.passwordHash, body.password))) {
      reply.code(401);
      return { message: "Invalid credentials" };
    }

    const { token, tokenHash, session } = issueSession(user.id);
    await createSessionRecord(session, tokenHash);
    reply.setCookie(SESSION_COOKIE_NAME, token, {
      ...sessionCookieOptions,
      expires: new Date(session.expiresAt)
    });

    await createAuditEvent(
      buildAuditEvent({
        actor: user,
        action: "auth.login",
        targetType: "session",
        targetId: session.id,
        detailKo: "사용자가 로그인했습니다."
      })
    );

    return authSessionResponseSchema.parse({
      user: toPublicUser(user),
      settings: (await getInstanceSettings()) ?? (await ensureSettings())
    });
  });

  app.post("/api/auth/logout", async (request, reply) => {
    const token = request.cookies[SESSION_COOKIE_NAME];
    if (token) {
      const record = await getSessionRecordByTokenHash(hashSessionToken(token));
      if (record) {
        const user = await getStoredUserById(record.payload.userId);
        if (user) {
          await createAuditEvent(
            buildAuditEvent({
              actor: user,
              action: "auth.logout",
              targetType: "session",
              targetId: record.id,
              detailKo: "사용자가 로그아웃했습니다."
            })
          );
        }
        await deleteSessionById(record.id);
      }
    }

    reply.clearCookie(SESSION_COOKIE_NAME, sessionCookieOptions);
    return { loggedOut: true };
  });

  app.get("/api/auth/session", async (request, reply) => {
    const auth = await resolveAuth(request, reply);
    if (!auth) {
      return { message: "Unauthorized" };
    }

    return authSessionResponseSchema.parse({
      user: toPublicUser(auth.user),
      settings: auth.settings
    });
  });

  app.get("/api/users", async (request, reply) => {
    const auth = await resolveAuth(request, reply, ["owner"]);
    if (!auth) {
      return { message: reply.statusCode === 403 ? "Forbidden" : "Unauthorized" };
    }

    return {
      items: (await listUsers()).map((user) => publicUserSchema.parse(user))
    };
  });

  app.post("/api/users", async (request, reply) => {
    const auth = await resolveAuth(request, reply, ["owner"]);
    if (!auth) {
      return { message: reply.statusCode === 403 ? "Forbidden" : "Unauthorized" };
    }

    const body = createUserRequestSchema.parse(request.body);
    const existing = await getStoredUserByEmail(body.email);
    if (existing) {
      reply.code(409);
      return { message: "User already exists" };
    }

    const now = new Date().toISOString();
    const user = buildStoredUser(
      {
        id: randomUUID(),
        email: body.email,
        name: body.name,
        role: body.role,
        isActive: true,
        createdAt: now,
        updatedAt: now
      },
      await hashPassword(body.password)
    );
    await saveStoredUser(user);
    await createAuditEvent(
      buildAuditEvent({
        actor: auth.user,
        action: "user.create",
        targetType: "user",
        targetId: user.id,
        detailKo: `${body.email} 사용자를 생성했습니다.`,
        metadata: { role: body.role }
      })
    );

    return { item: publicUserSchema.parse(toPublicUser(user)) };
  });

  app.put("/api/users/:id", async (request, reply) => {
    const auth = await resolveAuth(request, reply, ["owner"]);
    if (!auth) {
      return { message: reply.statusCode === 403 ? "Forbidden" : "Unauthorized" };
    }

    const params = request.params as { id: string };
    const existing = await getStoredUserById(params.id);
    if (!existing) {
      reply.code(404);
      return { message: "User not found" };
    }

    const body = updateUserRequestSchema.parse(request.body);
    const updated: StoredUser = {
      ...existing,
      name: body.name,
      role: body.role,
      isActive: body.isActive,
      passwordHash: body.password ? await hashPassword(body.password) : existing.passwordHash,
      updatedAt: new Date().toISOString()
    };
    await saveStoredUser(updated);
    await createAuditEvent(
      buildAuditEvent({
        actor: auth.user,
        action: "user.update",
        targetType: "user",
        targetId: updated.id,
        detailKo: `${updated.email} 사용자를 수정했습니다.`,
        metadata: { role: updated.role, isActive: updated.isActive }
      })
    );

    return { item: publicUserSchema.parse(toPublicUser(updated)) };
  });

  app.get("/api/settings", async (request, reply) => {
    const auth = await resolveAuth(request, reply);
    if (!auth) {
      return { message: "Unauthorized" };
    }

    return { item: auth.settings };
  });

  app.put("/api/settings", async (request, reply) => {
    const auth = await resolveAuth(request, reply, ["owner"]);
    if (!auth) {
      return { message: reply.statusCode === 403 ? "Forbidden" : "Unauthorized" };
    }

    const body = updateSettingsRequestSchema.parse(request.body);
    const nextSettings: InstanceSettings = {
      id: "default",
      ...body,
      updatedAt: new Date().toISOString(),
      updatedBy: auth.user.email
    };
    await saveInstanceSettings(nextSettings);
    await createAuditEvent(
      buildAuditEvent({
        actor: auth.user,
        action: "settings.update",
        targetType: "instance-settings",
        targetId: "default",
        detailKo: "인스턴스 설정을 수정했습니다.",
        metadata: body
      })
    );

    return { item: nextSettings };
  });

  app.get("/api/audit-logs", async (request, reply) => {
    const auth = await resolveAuth(request, reply, ["owner"]);
    if (!auth) {
      return { message: reply.statusCode === 403 ? "Forbidden" : "Unauthorized" };
    }

    return { items: await listAuditEvents() };
  });

  app.get("/api/jobs", async (request, reply) => {
    const auth = await resolveAuth(request, reply);
    if (!auth) {
      return { message: "Unauthorized" };
    }

    return { items: (await listRecentJobRuns()).map((item) => jobRunSchema.parse(item)) };
  });

  app.get("/api/jobs/:id", async (request, reply) => {
    const auth = await resolveAuth(request, reply);
    if (!auth) {
      return { message: "Unauthorized" };
    }

    const params = request.params as { id: string };
    const item = await getJobRunById(params.id);

    if (!item) {
      reply.code(404);
      return { message: "Job not found" };
    }

    return { item: jobRunSchema.parse(item) };
  });

  app.post("/api/jobs/eval", async (request, reply) => {
    const auth = await resolveAuth(request, reply, ["owner", "operator"]);
    if (!auth) {
      return { message: reply.statusCode === 403 ? "Forbidden" : "Unauthorized" };
    }

    return jobEnqueueResponseSchema.parse(await enqueueJob("eval", {}, auth.user));
  });

  app.post("/api/jobs/compare", async (request, reply) => {
    const auth = await resolveAuth(request, reply, ["owner", "operator"]);
    if (!auth) {
      return { message: reply.statusCode === 403 ? "Forbidden" : "Unauthorized" };
    }

    const payload = ((request.body as { experimentId?: string | null } | undefined) ?? {}) satisfies {
      experimentId?: string | null;
    };

    return jobEnqueueResponseSchema.parse(await enqueueJob("compare", payload, auth.user));
  });

  app.post("/api/jobs/compatibility", async (request, reply) => {
    const auth = await resolveAuth(request, reply, ["owner", "operator"]);
    if (!auth) {
      return { message: reply.statusCode === 403 ? "Forbidden" : "Unauthorized" };
    }

    const payload = ((request.body as { releaseCandidateId?: string | null } | undefined) ?? {}) satisfies {
      releaseCandidateId?: string | null;
    };

    return jobEnqueueResponseSchema.parse(await enqueueJob("compatibility", payload, auth.user));
  });

  app.post("/api/jobs/release-gate", async (request, reply) => {
    const auth = await resolveAuth(request, reply, ["owner", "operator"]);
    if (!auth) {
      return { message: reply.statusCode === 403 ? "Forbidden" : "Unauthorized" };
    }

    const payload = ((request.body as { releaseCandidateId?: string | null } | undefined) ?? {}) satisfies {
      releaseCandidateId?: string | null;
    };

    return jobEnqueueResponseSchema.parse(await enqueueJob("release-gate", payload, auth.user));
  });

  app.post("/api/jobs/artifact-export", async (request, reply) => {
    const auth = await resolveAuth(request, reply, ["owner", "operator"]);
    if (!auth) {
      return { message: reply.statusCode === 403 ? "Forbidden" : "Unauthorized" };
    }

    const payload = ((request.body as { releaseCandidateId?: string | null } | undefined) ?? {}) satisfies {
      releaseCandidateId?: string | null;
    };

    return jobEnqueueResponseSchema.parse(await enqueueJob("artifact-export", payload, auth.user));
  });

  app.get("/api/catalog", async (request, reply) => {
    const auth = await resolveAuth(request, reply);
    if (!auth) {
      return { message: "Unauthorized" };
    }

    return { items: await listCatalogEntries() };
  });

  app.get("/api/catalog/:id", async (request, reply) => {
    const auth = await resolveAuth(request, reply);
    if (!auth) {
      return { message: "Unauthorized" };
    }

    const params = request.params as { id: string };
    const item = await getCatalogEntryById(params.id);

    if (!item) {
      reply.code(404);
      return { message: "Catalog entry not found" };
    }

    return { item };
  });

  app.post("/api/catalog", async (request, reply) => {
    const auth = await resolveAuth(request, reply, ["owner", "operator"]);
    if (!auth) {
      return { message: reply.statusCode === 403 ? "Forbidden" : "Unauthorized" };
    }

    const catalogEntry = catalogEntrySchema.parse(request.body);
    await createCatalogEntry(catalogEntry);
    await createAuditEvent(
      buildAuditEvent({
        actor: auth.user,
        action: "catalog.create",
        targetType: "catalog-entry",
        targetId: catalogEntry.id,
        detailKo: `${catalogEntry.name} catalog entry를 생성했습니다.`
      })
    );
    return { saved: true };
  });

  app.put("/api/catalog/:id", async (request, reply) => {
    const auth = await resolveAuth(request, reply, ["owner", "operator"]);
    if (!auth) {
      return { message: reply.statusCode === 403 ? "Forbidden" : "Unauthorized" };
    }

    const catalogEntry = catalogEntrySchema.parse({
      ...(request.body as Parameters<typeof createCatalogEntry>[0]),
      id: (request.params as { id: string }).id
    });
    await updateCatalogEntry(catalogEntry);
    await createAuditEvent(
      buildAuditEvent({
        actor: auth.user,
        action: "catalog.update",
        targetType: "catalog-entry",
        targetId: catalogEntry.id,
        detailKo: `${catalogEntry.name} catalog entry를 수정했습니다.`
      })
    );
    return { saved: true };
  });

  app.delete("/api/catalog/:id", async (request, reply) => {
    const auth = await resolveAuth(request, reply, ["owner", "operator"]);
    if (!auth) {
      return { message: reply.statusCode === 403 ? "Forbidden" : "Unauthorized" };
    }

    const id = (request.params as { id: string }).id;
    await deleteCatalogEntry(id);
    await createAuditEvent(
      buildAuditEvent({
        actor: auth.user,
        action: "catalog.delete",
        targetType: "catalog-entry",
        targetId: id,
        detailKo: `${id} catalog entry를 삭제했습니다.`
      })
    );
    return { deleted: true };
  });

  app.post("/api/catalog/import", async (request, reply) => {
    const auth = await resolveAuth(request, reply, ["owner", "operator"]);
    if (!auth) {
      return { message: reply.statusCode === 403 ? "Forbidden" : "Unauthorized" };
    }

    const bundle = catalogImportBundleSchema.parse(request.body);
    await upsertCatalogImportBundle(bundle);
    await createAuditEvent(
      buildAuditEvent({
        actor: auth.user,
        action: "catalog.import",
        targetType: "catalog-bundle",
        detailKo: "catalog import bundle을 적용했습니다.",
        metadata: {
          catalogEntries: bundle.catalogEntries.length,
          evalCases: bundle.evalCases?.length ?? 0,
          releaseCandidates: bundle.releaseCandidates?.length ?? 0
        }
      })
    );
    return { saved: true };
  });

  app.get("/api/catalog/export", async (request, reply) => {
    const auth = await resolveAuth(request, reply);
    if (!auth) {
      return { message: "Unauthorized" };
    }

    return { item: catalogImportBundleSchema.parse(await exportCatalogImportBundle()) };
  });

  app.post("/api/manifests/validate", async (request, reply) => {
    const auth = await resolveAuth(request, reply);
    if (!auth) {
      return { message: "Unauthorized" };
    }

    const parsed = mcpManifestSchema.safeParse(request.body);
    return parsed.success
      ? { valid: true, issues: [], manifest: parsed.data }
      : {
          valid: false,
          issues: parsed.error.issues.map((issue) => `${issue.path.join(".")}: ${issue.message}`)
        };
  });

  app.post("/api/recommendations", async (request, reply) => {
    const auth = await resolveAuth(request, reply, ["owner", "operator"]);
    if (!auth) {
      return { message: reply.statusCode === 403 ? "Forbidden" : "Unauthorized" };
    }

    const parsed = recommendationRequestSchema.parse(request.body);
    const catalog = await listCatalogEntries();
    const result = recommendCatalog(parsed, catalog);
    await saveRecommendationRun(result);
    return result;
  });

  app.post("/api/recommendations/candidate", async (request, reply) => {
    const auth = await resolveAuth(request, reply, ["owner", "operator"]);
    if (!auth) {
      return { message: reply.statusCode === 403 ? "Forbidden" : "Unauthorized" };
    }

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

  app.get("/api/evals/latest", async (request, reply) => {
    const auth = await resolveAuth(request, reply);
    if (!auth) {
      return { message: "Unauthorized" };
    }

    return { latest: await getLatestEvalRun() };
  });

  app.get("/api/usage-events", async (request, reply) => {
    const auth = await resolveAuth(request, reply);
    if (!auth) {
      return { message: "Unauthorized" };
    }

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

  app.post("/api/usage-events", async (request, reply) => {
    const auth = await resolveAuth(request, reply, ["owner", "operator"]);
    if (!auth) {
      return { message: reply.statusCode === 403 ? "Forbidden" : "Unauthorized" };
    }

    const event = usageEventSchema.parse(request.body);
    await createUsageEvent(event);
    await createAuditEvent(
      buildAuditEvent({
        actor: auth.user,
        action: "usage-event.create",
        targetType: "usage-event",
        targetId: event.id,
        detailKo: `${event.action} usage event를 기록했습니다.`,
        metadata: { catalogId: event.catalogId }
      })
    );
    return { saved: true };
  });

  app.get("/api/feedback", async (request, reply) => {
    const auth = await resolveAuth(request, reply);
    if (!auth) {
      return { message: "Unauthorized" };
    }

    return { items: await listFeedbackRecords() };
  });

  app.post("/api/feedback", async (request, reply) => {
    const auth = await resolveAuth(request, reply, ["owner", "operator"]);
    if (!auth) {
      return { message: reply.statusCode === 403 ? "Forbidden" : "Unauthorized" };
    }

    const record = feedbackRecordSchema.parse(request.body);
    await createFeedbackRecord(record);
    await createAuditEvent(
      buildAuditEvent({
        actor: auth.user,
        action: "feedback.create",
        targetType: "feedback-record",
        targetId: record.id,
        detailKo: "운영자 피드백을 저장했습니다.",
        metadata: { catalogId: record.catalogId, scoreDelta: record.scoreDelta }
      })
    );
    return { saved: true };
  });

  app.get("/api/experiments", async (request, reply) => {
    const auth = await resolveAuth(request, reply);
    if (!auth) {
      return { message: "Unauthorized" };
    }

    return { items: await listExperiments() };
  });

  app.post("/api/experiments", async (request, reply) => {
    const auth = await resolveAuth(request, reply, ["owner", "operator"]);
    if (!auth) {
      return { message: reply.statusCode === 403 ? "Forbidden" : "Unauthorized" };
    }

    const experiment = experimentConfigSchema.parse(request.body);
    await createExperiment(experiment);
    await createAuditEvent(
      buildAuditEvent({
        actor: auth.user,
        action: "experiment.create",
        targetType: "experiment",
        targetId: experiment.id,
        detailKo: `${experiment.name} 실험을 생성했습니다.`
      })
    );
    return { saved: true };
  });

  app.put("/api/experiments/:id", async (request, reply) => {
    const auth = await resolveAuth(request, reply, ["owner", "operator"]);
    if (!auth) {
      return { message: reply.statusCode === 403 ? "Forbidden" : "Unauthorized" };
    }

    const experiment = experimentConfigSchema.parse({
      ...(request.body as object),
      id: (request.params as { id: string }).id
    });
    await updateExperiment(experiment);
    await createAuditEvent(
      buildAuditEvent({
        actor: auth.user,
        action: "experiment.update",
        targetType: "experiment",
        targetId: experiment.id,
        detailKo: `${experiment.name} 실험을 수정했습니다.`
      })
    );
    return { saved: true };
  });

  app.delete("/api/experiments/:id", async (request, reply) => {
    const auth = await resolveAuth(request, reply, ["owner", "operator"]);
    if (!auth) {
      return { message: reply.statusCode === 403 ? "Forbidden" : "Unauthorized" };
    }

    const id = (request.params as { id: string }).id;
    await deleteExperiment(id);
    await createAuditEvent(
      buildAuditEvent({
        actor: auth.user,
        action: "experiment.delete",
        targetType: "experiment",
        targetId: id,
        detailKo: `${id} 실험을 삭제했습니다.`
      })
    );
    return { deleted: true };
  });

  app.get("/api/compare/latest", async (request, reply) => {
    const auth = await resolveAuth(request, reply);
    if (!auth) {
      return { message: "Unauthorized" };
    }

    return { latest: await getLatestCompareRun() };
  });

  app.get("/api/release-candidates", async (request, reply) => {
    const auth = await resolveAuth(request, reply);
    if (!auth) {
      return { message: "Unauthorized" };
    }

    return { items: await listReleaseCandidates() };
  });

  app.post("/api/release-candidates", async (request, reply) => {
    const auth = await resolveAuth(request, reply, ["owner", "operator"]);
    if (!auth) {
      return { message: reply.statusCode === 403 ? "Forbidden" : "Unauthorized" };
    }

    const candidate = releaseCandidateSchema.parse(request.body);
    await createReleaseCandidate(candidate);
    await createAuditEvent(
      buildAuditEvent({
        actor: auth.user,
        action: "release-candidate.create",
        targetType: "release-candidate",
        targetId: candidate.id,
        detailKo: `${candidate.name} 릴리즈 후보를 생성했습니다.`
      })
    );
    return { saved: true };
  });

  app.put("/api/release-candidates/:id", async (request, reply) => {
    const auth = await resolveAuth(request, reply, ["owner", "operator"]);
    if (!auth) {
      return { message: reply.statusCode === 403 ? "Forbidden" : "Unauthorized" };
    }

    const candidate = releaseCandidateSchema.parse({
      ...(request.body as object),
      id: (request.params as { id: string }).id
    });
    await updateReleaseCandidate(candidate);
    await createAuditEvent(
      buildAuditEvent({
        actor: auth.user,
        action: "release-candidate.update",
        targetType: "release-candidate",
        targetId: candidate.id,
        detailKo: `${candidate.name} 릴리즈 후보를 수정했습니다.`
      })
    );
    return { saved: true };
  });

  app.delete("/api/release-candidates/:id", async (request, reply) => {
    const auth = await resolveAuth(request, reply, ["owner", "operator"]);
    if (!auth) {
      return { message: reply.statusCode === 403 ? "Forbidden" : "Unauthorized" };
    }

    const id = (request.params as { id: string }).id;
    await deleteReleaseCandidate(id);
    await createAuditEvent(
      buildAuditEvent({
        actor: auth.user,
        action: "release-candidate.delete",
        targetType: "release-candidate",
        targetId: id,
        detailKo: `${id} 릴리즈 후보를 삭제했습니다.`
      })
    );
    return { deleted: true };
  });

  app.get("/api/compatibility/latest", async (request, reply) => {
    const auth = await resolveAuth(request, reply);
    if (!auth) {
      return { message: "Unauthorized" };
    }

    return { latest: compatibilityReportSchema.nullable().parse(await getLatestCompatibilityReport()) };
  });

  app.get("/api/release-gate/latest", async (request, reply) => {
    const auth = await resolveAuth(request, reply);
    if (!auth) {
      return { message: "Unauthorized" };
    }

    return { latest: releaseGateReportSchema.nullable().parse(await getLatestGateReport()) };
  });

  app.get("/api/submission/latest", async (request, reply) => {
    const auth = await resolveAuth(request, reply);
    if (!auth) {
      return { message: "Unauthorized" };
    }

    return { latest: artifactExportSchema.nullable().parse(await getLatestArtifactExport()) };
  });

  return app;
}
