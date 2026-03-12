import { describe, it, expect, beforeEach, afterAll } from "vitest";
import { Test, TestingModule } from "@nestjs/testing";
import { INestApplication } from "@nestjs/common";
import request from "supertest";
import { AppModule } from "../../src/app.module";

describe("Auth & Books (E2E)", () => {
  let app: INestApplication;

  beforeEach(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();
    app = moduleFixture.createNestApplication();
    await app.init();
  });

  afterAll(async () => {
    if (app) await app.close();
  });

  it("should register, login, and access protected route", async () => {
    await request(app.getHttpServer())
      .post("/auth/register")
      .send({ username: "admin", password: "pass123", role: "ADMIN" })
      .expect(201);

    const loginRes = await request(app.getHttpServer())
      .post("/auth/login")
      .send({ username: "admin", password: "pass123" })
      .expect(200);

    expect(loginRes.body.token).toBeDefined();

    await request(app.getHttpServer())
      .post("/books")
      .set("Authorization", `Bearer ${loginRes.body.token}`)
      .send({ title: "Test", author: "A", publishedYear: 2023, genre: "F", price: 10 })
      .expect(201);
  });

  it("should reject unauthenticated book creation", async () => {
    await request(app.getHttpServer())
      .post("/books")
      .send({ title: "Test", author: "A", publishedYear: 2023, genre: "F", price: 10 })
      .expect(401);
  });

  it("should reject non-admin book creation", async () => {
    await request(app.getHttpServer())
      .post("/auth/register")
      .send({ username: "user", password: "pass123" });

    const loginRes = await request(app.getHttpServer())
      .post("/auth/login")
      .send({ username: "user", password: "pass123" });

    await request(app.getHttpServer())
      .post("/books")
      .set("Authorization", `Bearer ${loginRes.body.token}`)
      .send({ title: "Test", author: "A", publishedYear: 2023, genre: "F", price: 10 })
      .expect(403);
  });

  it("should allow public GET /books", async () => {
    await request(app.getHttpServer()).get("/books").expect(200);
  });
});
