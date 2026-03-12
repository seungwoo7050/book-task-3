import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { Test, TestingModule } from "@nestjs/testing";
import { TypeOrmModule } from "@nestjs/typeorm";
import { BooksService } from "../../src/books/books.service";
import { BooksModule } from "../../src/books/books.module";
import { Book } from "../../src/books/entities/book.entity";
import { NotFoundException } from "@nestjs/common";

describe("BooksService (with TypeORM)", () => {
  let module: TestingModule;
  let service: BooksService;

  beforeEach(async () => {
    module = await Test.createTestingModule({
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

    service = module.get(BooksService);
  });

  afterEach(async () => {
    await module.close();
  });

  const dto = {
    title: "Clean Code",
    author: "Robert C. Martin",
    publishedYear: 2008,
    genre: "Programming",
    price: 33.99,
  };

  it("should create and find a book", async () => {
    const book = await service.create(dto);
    expect(book.id).toBeDefined();

    const found = await service.findOne(book.id);
    expect(found.title).toBe("Clean Code");
  });

  it("should find all books", async () => {
    await service.create(dto);
    await service.create({ ...dto, title: "Refactoring" });

    const books = await service.findAll();
    expect(books).toHaveLength(2);
  });

  it("should throw NotFoundException", async () => {
    await expect(service.findOne("nonexistent")).rejects.toThrow(NotFoundException);
  });

  it("should update a book", async () => {
    const book = await service.create(dto);
    const updated = await service.update(book.id, { title: "Updated" });
    expect(updated.title).toBe("Updated");
  });

  it("should remove a book", async () => {
    const book = await service.create(dto);
    await service.remove(book.id);
    await expect(service.findOne(book.id)).rejects.toThrow(NotFoundException);
  });
});
