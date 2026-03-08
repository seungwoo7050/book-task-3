import { describe, it, expect, beforeEach, afterAll } from "vitest";
import { Test, TestingModule } from "@nestjs/testing";
import { INestApplication } from "@nestjs/common";
import request from "supertest";
import { AppModule } from "../../src/app.module";

describe("Books API (E2E)", () => {
  let app: INestApplication;

  beforeEach(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();
  });

  afterAll(async () => {
    if (app) {
      await app.close();
    }
  });

  describe("GET /books", () => {
    it("should return an empty array initially", async () => {
      const res = await request(app.getHttpServer()).get("/books");
      expect(res.status).toBe(200);
      expect(res.body).toEqual([]);
    });
  });

  describe("POST /books", () => {
    it("should create a book and return 201", async () => {
      const res = await request(app.getHttpServer())
        .post("/books")
        .send({
          title: "Clean Code",
          author: "Robert C. Martin",
          publishedYear: 2008,
          genre: "Software Engineering",
          price: 29.99,
        });

      expect(res.status).toBe(201);
      expect(res.body.id).toBeDefined();
      expect(res.body.title).toBe("Clean Code");
    });
  });

  describe("GET /books/:id", () => {
    it("should return a book by ID", async () => {
      const createRes = await request(app.getHttpServer())
        .post("/books")
        .send({
          title: "Test Book",
          author: "Author",
          publishedYear: 2023,
          genre: "Test",
          price: 20,
        });

      const res = await request(app.getHttpServer()).get(`/books/${createRes.body.id}`);
      expect(res.status).toBe(200);
      expect(res.body.title).toBe("Test Book");
    });

    it("should return 404 for non-existent book", async () => {
      const res = await request(app.getHttpServer()).get("/books/non-existent");
      expect(res.status).toBe(404);
    });
  });

  describe("PUT /books/:id", () => {
    it("should update an existing book", async () => {
      const createRes = await request(app.getHttpServer())
        .post("/books")
        .send({
          title: "Old Title",
          author: "Author",
          publishedYear: 2020,
          genre: "Fiction",
          price: 10,
        });

      const res = await request(app.getHttpServer())
        .put(`/books/${createRes.body.id}`)
        .send({ title: "New Title" });

      expect(res.status).toBe(200);
      expect(res.body.title).toBe("New Title");
      expect(res.body.author).toBe("Author");
    });

    it("should return 404 for non-existent book", async () => {
      const res = await request(app.getHttpServer())
        .put("/books/non-existent")
        .send({ title: "X" });
      expect(res.status).toBe(404);
    });
  });

  describe("DELETE /books/:id", () => {
    it("should delete a book and return 204", async () => {
      const createRes = await request(app.getHttpServer())
        .post("/books")
        .send({
          title: "To Delete",
          author: "Author",
          publishedYear: 2020,
          genre: "Fiction",
          price: 10,
        });

      const res = await request(app.getHttpServer()).delete(`/books/${createRes.body.id}`);
      expect(res.status).toBe(204);
    });

    it("should return 404 for non-existent book", async () => {
      const res = await request(app.getHttpServer()).delete("/books/non-existent");
      expect(res.status).toBe(404);
    });
  });
});
