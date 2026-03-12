import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { Test, TestingModule } from "@nestjs/testing";
import { INestApplication, ValidationPipe } from "@nestjs/common";
import request from "supertest";
import { AppModule } from "../../src/app.module";
import { HttpExceptionFilter } from "../../src/common/filters/http-exception.filter";
import { TransformInterceptor } from "../../src/common/interceptors/transform.interceptor";

describe("Pipeline E2E (NestJS)", () => {
  let app: INestApplication;

  beforeEach(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    app.useGlobalPipes(
      new ValidationPipe({
        whitelist: true,
        forbidNonWhitelisted: true,
        transform: true,
      }),
    );
    app.useGlobalFilters(new HttpExceptionFilter());
    app.useGlobalInterceptors(new TransformInterceptor());
    await app.init();
  });

  afterEach(async () => {
    await app.close();
  });

  const validBook = {
    title: "Clean Code",
    author: "Robert C. Martin",
    publishedYear: 2008,
    genre: "Programming",
    price: 33.99,
  };

  describe("Response wrapping", () => {
    it("should wrap GET response with { success, data }", async () => {
      const res = await request(app.getHttpServer()).get("/books");
      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(res.body.data).toEqual([]);
    });

    it("should wrap POST response", async () => {
      const res = await request(app.getHttpServer())
        .post("/books")
        .send(validBook);
      expect(res.status).toBe(201);
      expect(res.body.success).toBe(true);
      expect(res.body.data.title).toBe("Clean Code");
    });
  });

  describe("검증", () => {
    it("should reject missing required fields", async () => {
      const res = await request(app.getHttpServer())
        .post("/books")
        .send({ title: "Only Title" });
      expect(res.status).toBe(400);
      expect(res.body.success).toBe(false);
      expect(res.body.error.message).toBe("검증 실패");
      expect(res.body.error.details.length).toBeGreaterThan(0);
    });

    it("should reject invalid types", async () => {
      const res = await request(app.getHttpServer())
        .post("/books")
        .send({ ...validBook, publishedYear: "not-a-number" });
      expect(res.status).toBe(400);
      expect(res.body.success).toBe(false);
    });

    it("should reject unknown properties", async () => {
      const res = await request(app.getHttpServer())
        .post("/books")
        .send({ ...validBook, unknown: "field" });
      expect(res.status).toBe(400);
    });

    it("should allow valid partial update", async () => {
      const createRes = await request(app.getHttpServer())
        .post("/books")
        .send(validBook);
      const id = createRes.body.data.id;

      const res = await request(app.getHttpServer())
        .put(`/books/${id}`)
        .send({ title: "Updated" });
      expect(res.status).toBe(200);
      expect(res.body.data.title).toBe("Updated");
    });
  });

  describe("Error handling", () => {
    it("should return 404 in standard error envelope", async () => {
      const res = await request(app.getHttpServer()).get("/books/nonexistent");
      expect(res.status).toBe(404);
      expect(res.body.success).toBe(false);
      expect(res.body.error.statusCode).toBe(404);
    });
  });

  describe("Full CRUD", () => {
    it("should create, read, update, delete through pipeline", async () => {
      const createRes = await request(app.getHttpServer())
        .post("/books")
        .send(validBook);
      expect(createRes.status).toBe(201);
      const id = createRes.body.data.id;

      const getRes = await request(app.getHttpServer()).get(`/books/${id}`);
      expect(getRes.body.data.title).toBe("Clean Code");

      const updateRes = await request(app.getHttpServer())
        .put(`/books/${id}`)
        .send({ price: 29.99 });
      expect(updateRes.body.data.price).toBe(29.99);

      const deleteRes = await request(app.getHttpServer()).delete(`/books/${id}`);
      expect(deleteRes.status).toBe(204);

      const verifyRes = await request(app.getHttpServer()).get(`/books/${id}`);
      expect(verifyRes.status).toBe(404);
    });
  });
});
