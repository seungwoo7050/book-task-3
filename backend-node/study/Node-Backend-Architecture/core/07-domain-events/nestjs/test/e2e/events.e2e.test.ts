import { describe, it, expect, beforeAll, afterAll, vi } from "vitest";
import { Test } from "@nestjs/testing";
import { INestApplication, ValidationPipe } from "@nestjs/common";
import { EventEmitter2 } from "@nestjs/event-emitter";
import request from "supertest";
import { AppModule } from "../../src/app.module";
import { HttpExceptionFilter } from "../../src/common/filters/http-exception.filter";
import { TransformInterceptor } from "../../src/common/interceptors/transform.interceptor";

describe("Events E2E", () => {
  let app: INestApplication;
  let eventEmitter: EventEmitter2;

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

    eventEmitter = module.get(EventEmitter2);
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

  it("should emit book.created event on POST /books", async () => {
    const handler = vi.fn();
    eventEmitter.on("book.created", handler);

    const res = await request(app.getHttpServer()).post("/books").send(validBook);
    expect(res.status).toBe(201);

    expect(handler).toHaveBeenCalledOnce();
    expect(handler.mock.calls[0][0].title).toBe("Clean Code");

    eventEmitter.off("book.created", handler);
  });

  it("should emit book.updated event on PUT /books/:id", async () => {
    const handler = vi.fn();
    eventEmitter.on("book.updated", handler);

    const createRes = await request(app.getHttpServer()).post("/books").send(validBook);
    const id = createRes.body.data.id;

    const res = await request(app.getHttpServer()).put(`/books/${id}`).send({ price: 29.99 });
    expect(res.status).toBe(200);

    expect(handler).toHaveBeenCalledOnce();
    expect(handler.mock.calls[0][0].changes).toContain("price");

    eventEmitter.off("book.updated", handler);
  });

  it("should emit book.deleted event on DELETE /books/:id", async () => {
    const handler = vi.fn();
    eventEmitter.on("book.deleted", handler);

    const createRes = await request(app.getHttpServer()).post("/books").send(validBook);
    const id = createRes.body.data.id;

    const res = await request(app.getHttpServer()).delete(`/books/${id}`);
    expect(res.status).toBe(204);

    expect(handler).toHaveBeenCalledOnce();
    expect(handler.mock.calls[0][0].bookId).toBe(id);

    eventEmitter.off("book.deleted", handler);
  });

  it("should not emit events for invalid operations", async () => {
    const handler = vi.fn();
    eventEmitter.on("book.deleted", handler);

    await request(app.getHttpServer()).delete("/books/nonexistent");

    expect(handler).not.toHaveBeenCalled();

    eventEmitter.off("book.deleted", handler);
  });
});
