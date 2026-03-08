export const config = {
  port: Number(process.env.PORT ?? 3102),
  databaseUrl:
    process.env.DATABASE_URL ?? "postgres://postgres:postgres@127.0.0.1:5542/study1_v2"
};
