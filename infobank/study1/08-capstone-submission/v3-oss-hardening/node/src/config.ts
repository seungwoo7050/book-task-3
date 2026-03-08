export const config = {
  port: Number(process.env.PORT ?? 3103),
  databaseUrl:
    process.env.DATABASE_URL ?? "postgres://postgres:postgres@127.0.0.1:5543/study1_v3",
  appBaseUrl: process.env.APP_BASE_URL ?? "http://127.0.0.1:3003",
  sessionSecret: process.env.SESSION_SECRET ?? "study1-v3-session-secret",
  bootstrapOwnerEmail: process.env.BOOTSTRAP_OWNER_EMAIL ?? "owner@study1.local",
  bootstrapOwnerPassword: process.env.BOOTSTRAP_OWNER_PASSWORD ?? "ChangeMe123!",
  inlineJobWorker: process.env.INLINE_JOB_WORKER === "true"
};
