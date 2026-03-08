import { describe, it, expect, beforeEach, afterEach } from "vitest";
import request from "supertest";
import Database from "better-sqlite3";
import { Application } from "express";
import { createApp } from "../../src/app";
import { initDatabase } from "../../src/database/init";

describe("Database E2E", () => {
  let db: Database.Database;
  let app: Application;

  beforeEach(() => {
    db = new Database(":memory:");
    initDatabase(db);
    app = createApp(db);
  });

  afterEach(() => {
    db.close();
  });

  const validBook = {
    title: "Clean Code",
    author: "Robert C. Martin",
    publishedYear: 2008,
    genre: "Programming",
    price: 33.99,
  };

  it("should persist a book to the database", async () => {
    const createRes = await request(app).post("/books").send(validBook);
    expect(createRes.status).toBe(201);
    const id = createRes.body.data.id;

    // Verify directly from DB
    const row = db.prepare("SELECT * FROM books WHERE id = ?").get(id);
    expect(row).toBeDefined();
  });

  it("should retrieve all books from database", async () => {
    await request(app).post("/books").send(validBook);
    await request(app).post("/books").send({ ...validBook, title: "Refactoring" });

    const res = await request(app).get("/books");
    expect(res.status).toBe(200);
    expect(res.body.data).toHaveLength(2);
  });

  it("should update a book in the database", async () => {
    const createRes = await request(app).post("/books").send(validBook);
    const id = createRes.body.data.id;

    const updateRes = await request(app).put(`/books/${id}`).send({ price: 29.99 });
    expect(updateRes.status).toBe(200);
    expect(updateRes.body.data.price).toBe(29.99);

    // Verify from DB
    const row = db.prepare("SELECT price FROM books WHERE id = ?").get(id) as { price: number };
    expect(row.price).toBe(29.99);
  });

  it("should delete a book from the database", async () => {
    const createRes = await request(app).post("/books").send(validBook);
    const id = createRes.body.data.id;

    const deleteRes = await request(app).delete(`/books/${id}`);
    expect(deleteRes.status).toBe(204);

    const row = db.prepare("SELECT * FROM books WHERE id = ?").get(id);
    expect(row).toBeUndefined();
  });

  it("should return 404 for missing book", async () => {
    const res = await request(app).get("/books/nonexistent");
    expect(res.status).toBe(404);
    expect(res.body.success).toBe(false);
  });

  it("should validate request body", async () => {
    const res = await request(app).post("/books").send({ title: "Only Title" });
    expect(res.status).toBe(400);
    expect(res.body.success).toBe(false);
  });
});
