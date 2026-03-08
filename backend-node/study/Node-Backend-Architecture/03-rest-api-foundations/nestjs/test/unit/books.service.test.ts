import { describe, it, expect, beforeEach } from "vitest";
import { BooksService } from "../../src/books/books.service";
import { NotFoundException } from "@nestjs/common";

describe("BooksService", () => {
  let service: BooksService;

  beforeEach(() => {
    service = new BooksService();
  });

  it("should return an empty array when no books exist", () => {
    expect(service.findAll()).toEqual([]);
  });

  it("should create a book with a generated UUID", () => {
    const book = service.create({
      title: "Clean Code",
      author: "Robert C. Martin",
      publishedYear: 2008,
      genre: "Software Engineering",
      price: 29.99,
    });

    expect(book.id).toBeDefined();
    expect(book.title).toBe("Clean Code");
  });

  it("should find a book by ID", () => {
    const created = service.create({
      title: "Clean Code",
      author: "Robert C. Martin",
      publishedYear: 2008,
      genre: "Software Engineering",
      price: 29.99,
    });

    const found = service.findOne(created.id);
    expect(found).toEqual(created);
  });

  it("should throw NotFoundException for non-existent book", () => {
    expect(() => service.findOne("non-existent")).toThrow(NotFoundException);
  });

  it("should update an existing book", () => {
    const created = service.create({
      title: "Old Title",
      author: "Author",
      publishedYear: 2020,
      genre: "Fiction",
      price: 10,
    });

    const updated = service.update(created.id, { title: "New Title" });
    expect(updated.title).toBe("New Title");
    expect(updated.author).toBe("Author");
  });

  it("should throw NotFoundException when updating non-existent book", () => {
    expect(() => service.update("bad-id", { title: "X" })).toThrow(NotFoundException);
  });

  it("should remove an existing book", () => {
    const created = service.create({
      title: "To Delete",
      author: "Author",
      publishedYear: 2020,
      genre: "Fiction",
      price: 10,
    });

    service.remove(created.id);
    expect(() => service.findOne(created.id)).toThrow(NotFoundException);
  });

  it("should throw NotFoundException when removing non-existent book", () => {
    expect(() => service.remove("bad-id")).toThrow(NotFoundException);
  });
});
