import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { Test } from "@nestjs/testing";
import { type INestApplication } from "@nestjs/common";
import request from "supertest";
import { createClient, type RedisClientType } from "redis";
import { type DataSource } from "typeorm";

process.env.APP_NAME = process.env.APP_NAME || "shippable-backend-service-test";
process.env.NODE_ENV = process.env.NODE_ENV || "test";
process.env.PORT = process.env.PORT || "3100";
process.env.LOG_LEVEL = process.env.LOG_LEVEL || "error";
process.env.JWT_SECRET = process.env.JWT_SECRET || "test-secret";
process.env.DATABASE_URL =
  process.env.DATABASE_URL || "postgres://backend:backend@127.0.0.1:5432/shippable_backend";
process.env.REDIS_URL = process.env.REDIS_URL || "redis://127.0.0.1:6379";
process.env.LOGIN_THROTTLE_MAX_ATTEMPTS = process.env.LOGIN_THROTTLE_MAX_ATTEMPTS || "5";
process.env.LOGIN_THROTTLE_WINDOW_SECONDS =
  process.env.LOGIN_THROTTLE_WINDOW_SECONDS || "60";
process.env.BOOKS_CACHE_TTL_SECONDS = process.env.BOOKS_CACHE_TTL_SECONDS || "30";

describe("Shippable Backend Service E2E", () => {
  let app: INestApplication;
  let dataSource: DataSource;
  let redisClient: RedisClientType;
  let adminToken: string;

  const validBook = {
    title: "Clean Code",
    author: "Robert C. Martin",
    publishedYear: 2008,
    genre: "Programming",
    price: 33.99,
  };

  beforeAll(async () => {
    const [{ AppModule }, { configureApp }, { createAppDataSource }, { seedDatabase }] =
      await Promise.all([
        import("../../dist/app.module"),
        import("../../dist/app.bootstrap"),
        import("../../dist/database/data-source"),
        import("../../dist/database/seed-data"),
      ]);

    dataSource = createAppDataSource(process.env);
    await dataSource.initialize();
    await dataSource.dropDatabase();
    await dataSource.runMigrations();
    await seedDatabase(dataSource);

    redisClient = createClient({ url: process.env.REDIS_URL });
    await redisClient.connect();
    await redisClient.flushDb();

    const module = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = module.createNestApplication();
    await configureApp(app, { listen: false });

    const loginRes = await request(app.getHttpServer())
      .post("/auth/login")
      .send({ username: "admin", password: "admin123" });

    adminToken = loginRes.body.data.token;
  });

  afterAll(async () => {
    if (app) {
      await app.close();
    }
    if (redisClient?.isOpen) {
      await redisClient.quit();
    }
    if (dataSource?.isInitialized) {
      await dataSource.destroy();
    }
  });

  it("GET /health/live should return 200", async () => {
    const res = await request(app.getHttpServer()).get("/health/live");

    expect(res.status).toBe(200);
    expect(res.body.data.status).toBe("ok");
  });

  it("GET /health/ready should return 200 when Postgres and Redis are ready", async () => {
    const res = await request(app.getHttpServer()).get("/health/ready");

    expect(res.status).toBe(200);
    expect(res.body.data.databaseReady).toBe(true);
    expect(res.body.data.redisReady).toBe(true);
  });

  it("GET /docs should expose Swagger UI", async () => {
    const res = await request(app.getHttpServer()).get("/docs");

    expect(res.status).toBe(200);
    expect(res.text).toContain("swagger-ui");
  });

  it("POST /auth/register should register a regular user", async () => {
    const res = await request(app.getHttpServer())
      .post("/auth/register")
      .send({ username: "reader", password: "reader123" });

    expect(res.status).toBe(201);
    expect(res.body.data.username).toBe("reader");
  });

  it("POST /auth/register should reject duplicate username", async () => {
    const res = await request(app.getHttpServer())
      .post("/auth/register")
      .send({ username: "admin", password: "admin123" });

    expect(res.status).toBe(409);
  });

  it("POST /auth/login should return JWT token", async () => {
    const res = await request(app.getHttpServer())
      .post("/auth/login")
      .send({ username: "admin", password: "admin123" });

    expect(res.status).toBe(200);
    expect(res.body.data.token).toBeDefined();
  });

  it("POST /auth/login should throttle repeated failures", async () => {
    const clientId = "203.0.113.50";

    for (let index = 0; index < 4; index += 1) {
      const res = await request(app.getHttpServer())
        .post("/auth/login")
        .set("x-forwarded-for", clientId)
        .send({ username: "admin", password: "wrong-password" });

      expect(res.status).toBe(401);
    }

    const blocked = await request(app.getHttpServer())
      .post("/auth/login")
      .set("x-forwarded-for", clientId)
      .send({ username: "admin", password: "wrong-password" });

    expect(blocked.status).toBe(429);
  });

  it("GET /books should be public and populate the cache", async () => {
    const res = await request(app.getHttpServer()).get("/books");

    expect(res.status).toBe(200);
    expect(Array.isArray(res.body.data)).toBe(true);
    expect(await redisClient.get("books:list")).not.toBeNull();
  });

  it("GET /books/:id should populate a detail cache entry", async () => {
    const listRes = await request(app.getHttpServer()).get("/books");
    const bookId = listRes.body.data[0].id as string;

    const res = await request(app.getHttpServer()).get(`/books/${bookId}`);

    expect(res.status).toBe(200);
    expect(await redisClient.get(`books:detail:${bookId}`)).not.toBeNull();
  });

  it("POST /books should require authentication", async () => {
    const res = await request(app.getHttpServer())
      .post("/books")
      .send(validBook);

    expect(res.status).toBe(401);
  });

  it("POST /books should allow an admin to create a book and invalidate the list cache", async () => {
    await request(app.getHttpServer()).get("/books");
    expect(await redisClient.get("books:list")).not.toBeNull();

    const res = await request(app.getHttpServer())
      .post("/books")
      .set("Authorization", `Bearer ${adminToken}`)
      .send(validBook);

    expect(res.status).toBe(201);
    expect(res.body.data.title).toBe("Clean Code");
    expect(await redisClient.get("books:list")).toBeNull();
  });

  it("PUT /books/:id should update a book", async () => {
    const createRes = await request(app.getHttpServer())
      .post("/books")
      .set("Authorization", `Bearer ${adminToken}`)
      .send(validBook);
    const bookId = createRes.body.data.id as string;

    const res = await request(app.getHttpServer())
      .put(`/books/${bookId}`)
      .set("Authorization", `Bearer ${adminToken}`)
      .send({ price: 29.99 });

    expect(res.status).toBe(200);
    expect(res.body.data.price).toBe(29.99);
  });

  it("DELETE /books/:id should delete a book", async () => {
    const createRes = await request(app.getHttpServer())
      .post("/books")
      .set("Authorization", `Bearer ${adminToken}`)
      .send(validBook);
    const bookId = createRes.body.data.id as string;

    const res = await request(app.getHttpServer())
      .delete(`/books/${bookId}`)
      .set("Authorization", `Bearer ${adminToken}`);

    expect(res.status).toBe(204);
  });

  it("POST /books should return 403 for a regular user", async () => {
    await request(app.getHttpServer())
      .post("/auth/register")
      .send({ username: "member", password: "member123" });
    const loginRes = await request(app.getHttpServer())
      .post("/auth/login")
      .send({ username: "member", password: "member123" });
    const memberToken = loginRes.body.data.token as string;

    const res = await request(app.getHttpServer())
      .post("/books")
      .set("Authorization", `Bearer ${memberToken}`)
      .send(validBook);

    expect(res.status).toBe(403);
  });

  it("POST /books should reject invalid payloads", async () => {
    const res = await request(app.getHttpServer())
      .post("/books")
      .set("Authorization", `Bearer ${adminToken}`)
      .send({ title: "" });

    expect(res.status).toBe(400);
  });

  it("GET /books/:id should return 404 for a missing book", async () => {
    const res = await request(app.getHttpServer()).get("/books/00000000-0000-0000-0000-000000000000");

    expect(res.status).toBe(404);
  });
});
