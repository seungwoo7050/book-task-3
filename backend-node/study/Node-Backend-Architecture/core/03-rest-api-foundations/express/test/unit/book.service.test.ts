import { describe, it, expect, beforeEach } from "vitest";
import { BookService } from "../../src/services/book.service";

describe("BookService", () => {
  let service: BookService;

  beforeEach(() => {
    service = new BookService();
  });

  it("should return an empty array when no books exist", () => {
    expect(service.findAll()).toEqual([]);
  });

  it("should create a book with a generated UUID", () => {
    const dto = {
      title: "Clean Code",
      author: "Robert C. Martin",
      publishedYear: 2008,
      genre: "Software Engineering",
      price: 29.99,
    };

    const book = service.create(dto);

    expect(book.id).toBeDefined();
    expect(typeof book.id).toBe("string");
    expect(book.title).toBe("Clean Code");
    expect(book.author).toBe("Robert C. Martin");
    expect(book.publishedYear).toBe(2008);
    expect(book.genre).toBe("Software Engineering");
    expect(book.price).toBe(29.99);
  });

  it("should find a book by ID after creation", () => {
    const dto = {
      title: "Clean Code",
      author: "Robert C. Martin",
      publishedYear: 2008,
      genre: "Software Engineering",
      price: 29.99,
    };

    const created = service.create(dto);
    const found = service.findById(created.id);

    expect(found).toEqual(created);
  });

  it("should return undefined for a non-existent book", () => {
    expect(service.findById("non-existent-id")).toBeUndefined();
  });

  it("should return all created books", () => {
    service.create({
      title: "Book A",
      author: "Author A",
      publishedYear: 2020,
      genre: "Fiction",
      price: 10,
    });
    service.create({
      title: "Book B",
      author: "Author B",
      publishedYear: 2021,
      genre: "Non-Fiction",
      price: 15,
    });

    const all = service.findAll();
    expect(all).toHaveLength(2);
  });

  it("should update an existing book", () => {
    const created = service.create({
      title: "Old Title",
      author: "Author",
      publishedYear: 2020,
      genre: "Fiction",
      price: 10,
    });

    const updated = service.update(created.id, { title: "New Title", price: 20 });

    expect(updated).toBeDefined();
    expect(updated!.title).toBe("New Title");
    expect(updated!.price).toBe(20);
    expect(updated!.author).toBe("Author"); // Unchanged fields preserved
  });

  it("should return undefined when updating a non-existent book", () => {
    const result = service.update("no-such-id", { title: "X" });
    expect(result).toBeUndefined();
  });

  it("should delete an existing book", () => {
    const created = service.create({
      title: "To Delete",
      author: "Author",
      publishedYear: 2020,
      genre: "Fiction",
      price: 10,
    });

    const deleted = service.delete(created.id);
    expect(deleted).toBe(true);
    expect(service.findById(created.id)).toBeUndefined();
  });

  it("should return false when deleting a non-existent book", () => {
    expect(service.delete("no-such-id")).toBe(false);
  });
});
