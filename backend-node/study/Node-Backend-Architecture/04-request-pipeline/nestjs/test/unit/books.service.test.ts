import { describe, it, expect, beforeEach } from "vitest";
import { BooksService } from "../../src/books/books.service";
import { NotFoundException } from "@nestjs/common";

describe("BooksService", () => {
  let service: BooksService;

  beforeEach(() => {
    service = new BooksService();
  });

  const dto = {
    title: "Clean Code",
    author: "Robert C. Martin",
    publishedYear: 2008,
    genre: "Programming",
    price: 33.99,
  };

  it("should create a book", () => {
    const book = service.create(dto);
    expect(book.id).toBeDefined();
    expect(book.title).toBe("Clean Code");
  });

  it("should find all books", () => {
    service.create(dto);
    service.create({ ...dto, title: "Refactoring" });
    expect(service.findAll()).toHaveLength(2);
  });

  it("should find one by id", () => {
    const created = service.create(dto);
    expect(service.findOne(created.id).title).toBe("Clean Code");
  });

  it("should throw NotFoundException for missing book", () => {
    expect(() => service.findOne("nonexistent")).toThrow(NotFoundException);
  });

  it("should update a book", () => {
    const created = service.create(dto);
    const updated = service.update(created.id, { title: "Updated" });
    expect(updated.title).toBe("Updated");
    expect(updated.author).toBe("Robert C. Martin");
  });

  it("should remove a book", () => {
    const created = service.create(dto);
    service.remove(created.id);
    expect(service.findAll()).toHaveLength(0);
  });

  it("should throw NotFoundException when removing missing book", () => {
    expect(() => service.remove("nonexistent")).toThrow(NotFoundException);
  });
});
