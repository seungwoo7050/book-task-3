import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { Test, TestingModule } from "@nestjs/testing";
import { INestApplication, ValidationPipe } from "@nestjs/common";
import { TypeOrmModule } from "@nestjs/typeorm";
import request from "supertest";
import { BooksModule } from "../../src/books/books.module";
import { Book } from "../../src/books/entities/book.entity";
import { HttpExceptionFilter } from "../../src/common/filters/http-exception.filter";
import { TransformInterceptor } from "../../src/common/interceptors/transform.interceptor";

describe("Database E2E (NestJS)", () => {
  let app: INestApplication;

  beforeEach(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [
        TypeOrmModule.forRoot({
          type: "better-sqlite3",
          database: ":memory:",
          entities: [Book],
          synchronize: true,
        }),
        BooksModule,
      ],
    }).compile();

    app = moduleFixture.createNestApplication();
    app.useGlobalPipes(new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, transform: true }));
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

  it("should create a book and persist it", async () => {
    const res = await request(app.getHttpServer()).post("/books").send(validBook);
    expect(res.status).toBe(201);
    expect(res.body.success).toBe(true);

    const id = res.body.data.id;
    const getRes = await request(app.getHttpServer()).get(`/books/${id}`);
    expect(getRes.body.data.title).toBe("Clean Code");
  });

  it("should list all books", async () => {
    await request(app.getHttpServer()).post("/books").send(validBook);
    await request(app.getHttpServer()).post("/books").send({ ...validBook, title: "Refactoring" });

    const res = await request(app.getHttpServer()).get("/books");
    expect(res.body.data).toHaveLength(2);
  });

  it("should update a book", async () => {
    const createRes = await request(app.getHttpServer()).post("/books").send(validBook);
    const id = createRes.body.data.id;

    const updateRes = await request(app.getHttpServer()).put(`/books/${id}`).send({ price: 29.99 });
    expect(updateRes.body.data.price).toBe(29.99);
  });

  it("should delete a book", async () => {
    const createRes = await request(app.getHttpServer()).post("/books").send(validBook);
    const id = createRes.body.data.id;

    await request(app.getHttpServer()).delete(`/books/${id}`).expect(204);

    const verifyRes = await request(app.getHttpServer()).get(`/books/${id}`);
    expect(verifyRes.status).toBe(404);
  });

  it("should return 404 for missing book", async () => {
    const res = await request(app.getHttpServer()).get("/books/nonexistent");
    expect(res.status).toBe(404);
    expect(res.body.success).toBe(false);
  });

  it("should validate input", async () => {
    const res = await request(app.getHttpServer()).post("/books").send({ title: "Only" });
    expect(res.status).toBe(400);
    expect(res.body.success).toBe(false);
  });
});
