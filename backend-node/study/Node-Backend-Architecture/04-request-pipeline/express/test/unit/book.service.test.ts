import { describe, it, expect, beforeEach } from "vitest";
import { BookService } from "../../src/services/book.service";
import { NotFoundError } from "../../src/errors";

describe("BookService", () => {
  let service: BookService;

  beforeEach(() => {
    service = new BookService();
  });

  describe("create", () => {
    it("should create a book and return it with id", () => {
      const dto = {
        title: "Clean Code",
        author: "Robert C. Martin",
        publishedYear: 2008,
        genre: "Programming",
        price: 33.99,
      };
      const book = service.create(dto);

      expect(book.id).toBeDefined();
      expect(book.title).toBe("Clean Code");
      expect(book.createdAt).toBeInstanceOf(Date);
      expect(book.updatedAt).toBeInstanceOf(Date);
    });
  });

  describe("findAll", () => {
    it("should return empty array when no books", () => {
      expect(service.findAll()).toEqual([]);
    });

    it("should return all created books", () => {
      service.create({ title: "A", author: "X", publishedYear: 2000, genre: "Fiction", price: 10 });
      service.create({ title: "B", author: "Y", publishedYear: 2001, genre: "Fiction", price: 20 });

      expect(service.findAll()).toHaveLength(2);
    });
  });

  describe("findById", () => {
    it("should return the book when found", () => {
      const created = service.create({ title: "A", author: "X", publishedYear: 2000, genre: "Fiction", price: 10 });
      const found = service.findById(created.id);

      expect(found.id).toBe(created.id);
    });

    it("should throw NotFoundError when not found", () => {
      expect(() => service.findById("nonexistent")).toThrow(NotFoundError);
    });
  });

  describe("update", () => {
    it("should update partial fields", () => {
      const created = service.create({ title: "Old", author: "X", publishedYear: 2000, genre: "Fiction", price: 10 });
      const updated = service.update(created.id, { title: "New" });

      expect(updated.title).toBe("New");
      expect(updated.author).toBe("X");
      expect(updated.updatedAt.getTime()).toBeGreaterThanOrEqual(created.updatedAt.getTime());
    });

    it("should throw NotFoundError for missing book", () => {
      expect(() => service.update("nonexistent", { title: "X" })).toThrow(NotFoundError);
    });
  });

  describe("delete", () => {
    it("should remove the book", () => {
      const created = service.create({ title: "A", author: "X", publishedYear: 2000, genre: "Fiction", price: 10 });
      service.delete(created.id);

      expect(service.findAll()).toHaveLength(0);
    });

    it("should throw NotFoundError for missing book", () => {
      expect(() => service.delete("nonexistent")).toThrow(NotFoundError);
    });
  });
});
