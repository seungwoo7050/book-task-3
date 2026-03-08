import { describe, it, expect, beforeEach } from "vitest";
import request from "supertest";
import { createApp } from "../../src/app";
import type { Express } from "express";

describe("Books API (E2E)", () => {
  let app: Express;

  beforeEach(() => {
    app = createApp(); // Fresh app with empty in-memory store each test
  });

  describe("GET /books", () => {
    it("should return an empty array initially", async () => {
      const res = await request(app).get("/books");

      expect(res.status).toBe(200);
      expect(res.body).toEqual([]);
    });

    it("should return all created books", async () => {
      await request(app).post("/books").send({
        title: "Book A",
        author: "Author A",
        publishedYear: 2020,
        genre: "Fiction",
        price: 10,
      });

      await request(app).post("/books").send({
        title: "Book B",
        author: "Author B",
        publishedYear: 2021,
        genre: "Non-Fiction",
        price: 15,
      });

      const res = await request(app).get("/books");

      expect(res.status).toBe(200);
      expect(res.body).toHaveLength(2);
    });
  });

  describe("POST /books", () => {
    it("should create a book and return 201", async () => {
      const newBook = {
        title: "Clean Code",
        author: "Robert C. Martin",
        publishedYear: 2008,
        genre: "Software Engineering",
        price: 29.99,
      };

      const res = await request(app).post("/books").send(newBook);

      expect(res.status).toBe(201);
      expect(res.body.id).toBeDefined();
      expect(res.body.title).toBe("Clean Code");
      expect(res.body.author).toBe("Robert C. Martin");
    });
  });

  describe("GET /books/:id", () => {
    it("should return a book by ID", async () => {
      const createRes = await request(app).post("/books").send({
        title: "Test Book",
        author: "Test Author",
        publishedYear: 2023,
        genre: "Test",
        price: 20,
      });

      const res = await request(app).get(`/books/${createRes.body.id}`);

      expect(res.status).toBe(200);
      expect(res.body.title).toBe("Test Book");
    });

    it("should return 404 for non-existent book", async () => {
      const res = await request(app).get("/books/non-existent-id");

      expect(res.status).toBe(404);
      expect(res.body.error).toBe("Book not found");
    });
  });

  describe("PUT /books/:id", () => {
    it("should update an existing book", async () => {
      const createRes = await request(app).post("/books").send({
        title: "Old Title",
        author: "Author",
        publishedYear: 2020,
        genre: "Fiction",
        price: 10,
      });

      const res = await request(app)
        .put(`/books/${createRes.body.id}`)
        .send({ title: "New Title" });

      expect(res.status).toBe(200);
      expect(res.body.title).toBe("New Title");
      expect(res.body.author).toBe("Author"); // Unchanged
    });

    it("should return 404 for non-existent book", async () => {
      const res = await request(app)
        .put("/books/non-existent-id")
        .send({ title: "X" });

      expect(res.status).toBe(404);
    });
  });

  describe("DELETE /books/:id", () => {
    it("should delete an existing book and return 204", async () => {
      const createRes = await request(app).post("/books").send({
        title: "To Delete",
        author: "Author",
        publishedYear: 2020,
        genre: "Fiction",
        price: 10,
      });

      const res = await request(app).delete(`/books/${createRes.body.id}`);

      expect(res.status).toBe(204);

      // Verify deletion
      const getRes = await request(app).get(`/books/${createRes.body.id}`);
      expect(getRes.status).toBe(404);
    });

    it("should return 404 for non-existent book", async () => {
      const res = await request(app).delete("/books/non-existent-id");

      expect(res.status).toBe(404);
    });
  });
});
