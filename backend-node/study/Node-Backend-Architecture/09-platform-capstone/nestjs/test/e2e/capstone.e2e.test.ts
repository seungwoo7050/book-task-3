import { describe, it, expect, beforeAll, afterAll } from "vitest";
import { Test } from "@nestjs/testing";
import { INestApplication, ValidationPipe } from "@nestjs/common";
import request from "supertest";
import { AppModule } from "../../src/app.module";
import { HttpExceptionFilter } from "../../src/common/filters/http-exception.filter";
import { TransformInterceptor } from "../../src/common/interceptors/transform.interceptor";

describe("Platform Capstone E2E", () => {
  let app: INestApplication;
  let adminToken: string;

  beforeAll(async () => {
    process.env.DB_PATH = ":memory:";

    const module = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = module.createNestApplication();
    app.useGlobalPipes(
      new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, transform: true }),
    );
    app.useGlobalFilters(new HttpExceptionFilter());
    app.useGlobalInterceptors(new TransformInterceptor());
    await app.init();

    // Register admin user
    await request(app.getHttpServer())
      .post("/auth/register")
      .send({ username: "admin", password: "admin123", role: "ADMIN" });

    // Login to get token
    const loginRes = await request(app.getHttpServer())
      .post("/auth/login")
      .send({ username: "admin", password: "admin123" });

    adminToken = loginRes.body.data.token;
  });

  afterAll(async () => {
    await app.close();
  });

  const validBook = {
    title: "Clean Code",
    author: "Robert C. Martin",
    publishedYear: 2008,
    genre: "Programming",
    price: 33.99,
  };

  // --- Auth Tests ---

  it("POST /auth/register — should register a new user", async () => {
    const res = await request(app.getHttpServer())
      .post("/auth/register")
      .send({ username: "testuser", password: "test123456" });

    expect(res.status).toBe(201);
    expect(res.body.data.username).toBe("testuser");
  });

  it("POST /auth/register — should reject duplicate username", async () => {
    const res = await request(app.getHttpServer())
      .post("/auth/register")
      .send({ username: "admin", password: "admin123" });

    expect(res.status).toBe(409);
  });

  it("POST /auth/login — should return JWT token", async () => {
    const res = await request(app.getHttpServer())
      .post("/auth/login")
      .send({ username: "admin", password: "admin123" });

    expect(res.status).toBe(200);
    expect(res.body.data.token).toBeDefined();
  });

  it("POST /auth/login — should reject invalid credentials", async () => {
    const res = await request(app.getHttpServer())
      .post("/auth/login")
      .send({ username: "admin", password: "wrong" });

    expect(res.status).toBe(401);
  });

  // --- Public Book Routes ---

  it("GET /books — should be public", async () => {
    const res = await request(app.getHttpServer()).get("/books");
    expect(res.status).toBe(200);
    expect(res.body.success).toBe(true);
  });

  // --- Protected Book Routes ---

  it("POST /books — should require authentication", async () => {
    const res = await request(app.getHttpServer())
      .post("/books")
      .send(validBook);

    expect(res.status).toBe(401);
  });

  it("POST /books — admin should create a book", async () => {
    const res = await request(app.getHttpServer())
      .post("/books")
      .set("Authorization", `Bearer ${adminToken}`)
      .send(validBook);

    expect(res.status).toBe(201);
    expect(res.body.data.title).toBe("Clean Code");
  });

  it("PUT /books/:id — admin should update a book", async () => {
    const createRes = await request(app.getHttpServer())
      .post("/books")
      .set("Authorization", `Bearer ${adminToken}`)
      .send(validBook);

    const id = createRes.body.data.id;

    const res = await request(app.getHttpServer())
      .put(`/books/${id}`)
      .set("Authorization", `Bearer ${adminToken}`)
      .send({ price: 29.99 });

    expect(res.status).toBe(200);
    expect(res.body.data.price).toBe(29.99);
  });

  it("DELETE /books/:id — admin should delete a book", async () => {
    const createRes = await request(app.getHttpServer())
      .post("/books")
      .set("Authorization", `Bearer ${adminToken}`)
      .send(validBook);

    const id = createRes.body.data.id;

    const res = await request(app.getHttpServer())
      .delete(`/books/${id}`)
      .set("Authorization", `Bearer ${adminToken}`);

    expect(res.status).toBe(204);
  });

  // --- Role-Based Access ---

  it("POST /books — regular user should be forbidden", async () => {
    // Register a regular user
    await request(app.getHttpServer())
      .post("/auth/register")
      .send({ username: "regularuser", password: "regular123" });

    const loginRes = await request(app.getHttpServer())
      .post("/auth/login")
      .send({ username: "regularuser", password: "regular123" });

    const userToken = loginRes.body.data.token;

    const res = await request(app.getHttpServer())
      .post("/books")
      .set("Authorization", `Bearer ${userToken}`)
      .send(validBook);

    expect(res.status).toBe(403);
  });

  // --- Validation ---

  it("POST /books — should reject invalid body", async () => {
    const res = await request(app.getHttpServer())
      .post("/books")
      .set("Authorization", `Bearer ${adminToken}`)
      .send({ title: "" });

    expect(res.status).toBe(400);
  });

  // --- Not Found ---

  it("GET /books/:id — should return 404 for missing book", async () => {
    const res = await request(app.getHttpServer()).get("/books/nonexistent");

    expect(res.status).toBe(404);
  });
});
