export const config = {
  port: Number(process.env.PORT ?? 3101),
  databaseUrl:
    process.env.DATABASE_URL ?? "postgres://postgres:postgres@127.0.0.1:5541/study1_v1"
};
