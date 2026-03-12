import { describe, it, expect, beforeEach } from "vitest";
import request from "supertest";
import { createApp } from "../../src/app";
import type { Express } from "express";

describe("Auth API (E2E)", () => {
  let app: Express;

  beforeEach(() => {
    app = createApp();
  });

  describe("POST /auth/register", () => {
    it("should register a new user and return 201", async () => {
      const res = await request(app)
        .post("/auth/register")
        .send({ username: "john", password: "pass123" });

      expect(res.status).toBe(201);
      expect(res.body.username).toBe("john");
      expect(res.body.role).toBe("USER");
      expect(res.body.password).toBeUndefined();
    });

    it("should register an admin user", async () => {
      const res = await request(app)
        .post("/auth/register")
        .send({ username: "admin", password: "pass123", role: "ADMIN" });

      expect(res.status).toBe(201);
      expect(res.body.role).toBe("ADMIN");
    });

    it("should return 409 for duplicate username", async () => {
      await request(app)
        .post("/auth/register")
        .send({ username: "john", password: "pass123" });

      const res = await request(app)
        .post("/auth/register")
        .send({ username: "john", password: "other" });

      expect(res.status).toBe(409);
    });
  });

  describe("POST /auth/login", () => {
    it("should login and return a JWT", async () => {
      await request(app)
        .post("/auth/register")
        .send({ username: "john", password: "pass123" });

      const res = await request(app)
        .post("/auth/login")
        .send({ username: "john", password: "pass123" });

      expect(res.status).toBe(200);
      expect(res.body.token).toBeDefined();
      expect(res.body.user.username).toBe("john");
    });

    it("should return 401 for invalid credentials", async () => {
      const res = await request(app)
        .post("/auth/login")
        .send({ username: "nonexistent", password: "wrong" });

      expect(res.status).toBe(401);
    });
  });

  describe("Protected 라우트", () => {
    let adminToken: string;

    beforeEach(async () => {
      await request(app)
        .post("/auth/register")
        .send({ username: "admin", password: "pass123", role: "ADMIN" });

      const loginRes = await request(app)
        .post("/auth/login")
        .send({ username: "admin", password: "pass123" });

      adminToken = loginRes.body.token;
    });

    it("should allow admin to create a book", async () => {
      const res = await request(app)
        .post("/books")
        .set("Authorization", `Bearer ${adminToken}`)
        .send({
          title: "Test Book",
          author: "Author",
          publishedYear: 2023,
          genre: "Fiction",
          price: 20,
        });

      expect(res.status).toBe(201);
    });

    it("should reject unauthenticated requests to protected routes", async () => {
      const res = await request(app)
        .post("/books")
        .send({ title: "Test", author: "A", publishedYear: 2023, genre: "F", price: 10 });

      expect(res.status).toBe(401);
    });

    it("should reject non-admin users from protected routes", async () => {
      await request(app)
        .post("/auth/register")
        .send({ username: "user", password: "pass123", role: "USER" });

      const loginRes = await request(app)
        .post("/auth/login")
        .send({ username: "user", password: "pass123" });

      const res = await request(app)
        .post("/books")
        .set("Authorization", `Bearer ${loginRes.body.token}`)
        .send({ title: "Test", author: "A", publishedYear: 2023, genre: "F", price: 10 });

      expect(res.status).toBe(403);
    });

    it("should allow public access to GET /books", async () => {
      const res = await request(app).get("/books");
      expect(res.status).toBe(200);
    });
  });
});
