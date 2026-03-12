import { describe, it, expect, beforeEach, afterEach } from "vitest";
import Database from "better-sqlite3";
import { BookRepository } from "../../src/repositories/book.repository";
import { initDatabase } from "../../src/database/init";
import { Book } from "../../src/types/book";

describe("BookRepository", () => {
  let db: Database.Database;
  let repo: BookRepository;

  beforeEach(() => {
    db = new Database(":memory:");
    initDatabase(db);
    repo = new BookRepository(db);
  });

  afterEach(() => {
    db.close();
  });

  const makeBook = (overrides?: Partial<Book>): Book => ({
    id: "test-id",
    title: "Clean Code",
    author: "Robert C. Martin",
    publishedYear: 2008,
    genre: "Programming",
    price: 33.99,
    createdAt: new Date("2024-01-01T00:00:00Z"),
    updatedAt: new Date("2024-01-01T00:00:00Z"),
    ...overrides,
  });

  it("should create and find a book", () => {
    const book = makeBook();
    repo.create(book);
    const found = repo.findById("test-id");

    expect(found).not.toBeNull();
    expect(found!.title).toBe("Clean Code");
    expect(found!.createdAt).toBeInstanceOf(Date);
  });

  it("should return null for missing book", () => {
    expect(repo.findById("nonexistent")).toBeNull();
  });

  it("should find all books", () => {
    repo.create(makeBook({ id: "1" }));
    repo.create(makeBook({ id: "2", title: "Refactoring" }));

    const books = repo.findAll();
    expect(books).toHaveLength(2);
  });

  it("should update a book", () => {
    repo.create(makeBook());
    const updated = repo.update("test-id", { title: "Updated Title" });

    expect(updated).not.toBeNull();
    expect(updated!.title).toBe("Updated Title");
    expect(updated!.author).toBe("Robert C. Martin");
  });

  it("should return null when updating missing book", () => {
    expect(repo.update("nonexistent", { title: "X" })).toBeNull();
  });

  it("should delete a book", () => {
    repo.create(makeBook());
    expect(repo.delete("test-id")).toBe(true);
    expect(repo.findById("test-id")).toBeNull();
  });

  it("should return false when deleting missing book", () => {
    expect(repo.delete("nonexistent")).toBe(false);
  });
});
