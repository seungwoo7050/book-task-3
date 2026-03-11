export const config = {
  port: Number(process.env.PORT ?? 3100),
  databaseUrl:
    process.env.DATABASE_URL ?? "postgres://postgres:postgres@127.0.0.1:5540/study1_v0"
};
