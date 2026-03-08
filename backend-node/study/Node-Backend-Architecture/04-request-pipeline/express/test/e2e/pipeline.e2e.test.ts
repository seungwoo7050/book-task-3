import { describe, it, expect, beforeEach } from "vitest";
import request from "supertest";
import { createApp } from "../../src/app";
import { Application } from "express";

describe("Pipeline E2E", () => {
  let app: Application;

  beforeEach(() => {
    app = createApp();
  });

  const validBook = {
    title: "Clean Code",
    author: "Robert C. Martin",
    publishedYear: 2008,
    genre: "Programming",
    price: 33.99,
  };

  // --- Response Wrapper ---
  describe("Response Wrapper", () => {
    it("should wrap successful GET response with { success, data }", async () => {
      const res = await request(app).get("/books");

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(res.body.data).toEqual([]);
    });

    it("should wrap successful POST response", async () => {
      const res = await request(app).post("/books").send(validBook);

      expect(res.status).toBe(201);
      expect(res.body.success).toBe(true);
      expect(res.body.data.title).toBe("Clean Code");
      expect(res.body.data.id).toBeDefined();
    });
  });

  // --- Validation ---
  describe("Validation", () => {
    it("should reject body with missing required fields", async () => {
      const res = await request(app).post("/books").send({ title: "Only Title" });

      expect(res.status).toBe(400);
      expect(res.body.success).toBe(false);
      expect(res.body.error.message).toBe("Validation failed");
      expect(res.body.error.details.length).toBeGreaterThan(0);
    });

    it("should reject body with invalid types", async () => {
      const res = await request(app)
        .post("/books")
        .send({ ...validBook, publishedYear: "not-a-number" });

      expect(res.status).toBe(400);
      expect(res.body.success).toBe(false);
      const fields = res.body.error.details.map((d: { field: string }) => d.field);
      expect(fields).toContain("publishedYear");
    });

    it("should reject negative price", async () => {
      const res = await request(app)
        .post("/books")
        .send({ ...validBook, price: -10 });

      expect(res.status).toBe(400);
    });

    it("should allow valid partial update", async () => {
      const createRes = await request(app).post("/books").send(validBook);
      const id = createRes.body.data.id;

      const res = await request(app)
        .put(`/books/${id}`)
        .send({ title: "Updated Title" });

      expect(res.status).toBe(200);
      expect(res.body.data.title).toBe("Updated Title");
    });
  });

  // --- Error Handling ---
  describe("Error Handling", () => {
    it("should return 404 with standard error envelope for missing book", async () => {
      const res = await request(app).get("/books/nonexistent");

      expect(res.status).toBe(404);
      expect(res.body.success).toBe(false);
      expect(res.body.error.statusCode).toBe(404);
      expect(res.body.error.message).toContain("not found");
    });

    it("should return 404 for delete on missing book", async () => {
      const res = await request(app).delete("/books/nonexistent");

      expect(res.status).toBe(404);
      expect(res.body.success).toBe(false);
    });
  });

  // --- Full CRUD with pipeline ---
  describe("Full CRUD through pipeline", () => {
    it("should create, read, update, and delete a book", async () => {
      // Create
      const createRes = await request(app).post("/books").send(validBook);
      expect(createRes.status).toBe(201);
      const id = createRes.body.data.id;

      // Read
      const getRes = await request(app).get(`/books/${id}`);
      expect(getRes.status).toBe(200);
      expect(getRes.body.data.title).toBe("Clean Code");

      // Update
      const updateRes = await request(app)
        .put(`/books/${id}`)
        .send({ price: 29.99 });
      expect(updateRes.status).toBe(200);
      expect(updateRes.body.data.price).toBe(29.99);

      // Delete
      const deleteRes = await request(app).delete(`/books/${id}`);
      expect(deleteRes.status).toBe(204);

      // Verify deleted
      const verifyRes = await request(app).get(`/books/${id}`);
      expect(verifyRes.status).toBe(404);
    });
  });
});
