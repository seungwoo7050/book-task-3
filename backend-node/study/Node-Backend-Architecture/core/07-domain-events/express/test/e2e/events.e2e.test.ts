import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import request from "supertest";
import Database from "better-sqlite3";
import { Application } from "express";
import { createApp } from "../../src/app";
import { initDatabase } from "../../src/database/init";
import { EventBus } from "../../src/events/event-bus";

describe("Event System E2E", () => {
  let db: Database.Database;
  let app: Application;
  let eventBus: EventBus;

  beforeEach(() => {
    db = new Database(":memory:");
    initDatabase(db);
    eventBus = new EventBus();
    app = createApp(db, eventBus);
  });

  afterEach(() => {
    eventBus.removeAllListeners();
    db.close();
  });

  const validBook = {
    title: "Clean Code",
    author: "Robert C. Martin",
    publishedYear: 2008,
    genre: "Programming",
    price: 33.99,
  };

  it("should emit book.created event on POST", async () => {
    const handler = vi.fn();
    eventBus.on("book.created", handler);

    await request(app).post("/books").send(validBook);

    expect(handler).toHaveBeenCalledOnce();
    expect(handler.mock.calls[0][0]).toMatchObject({
      title: "Clean Code",
      author: "Robert C. Martin",
    });
  });

  it("should emit book.updated event on PUT", async () => {
    const handler = vi.fn();
    eventBus.on("book.updated", handler);

    const createRes = await request(app).post("/books").send(validBook);
    const id = createRes.body.data.id;

    await request(app).put(`/books/${id}`).send({ price: 29.99 });

    expect(handler).toHaveBeenCalledOnce();
    expect(handler.mock.calls[0][0].changes).toContain("price");
  });

  it("should emit book.deleted event on DELETE", async () => {
    const handler = vi.fn();
    eventBus.on("book.deleted", handler);

    const createRes = await request(app).post("/books").send(validBook);
    const id = createRes.body.data.id;

    await request(app).delete(`/books/${id}`);

    expect(handler).toHaveBeenCalledOnce();
    expect(handler.mock.calls[0][0].bookId).toBe(id);
  });

  it("should not emit events on failed operations", async () => {
    const handler = vi.fn();
    eventBus.on("book.deleted", handler);

    await request(app).delete("/books/nonexistent");

    expect(handler).not.toHaveBeenCalled();
  });

  it("should still persist data with events", async () => {
    const createRes = await request(app).post("/books").send(validBook);
    expect(createRes.status).toBe(201);

    const id = createRes.body.data.id;
    const getRes = await request(app).get(`/books/${id}`);
    expect(getRes.body.data.title).toBe("Clean Code");
  });
});
