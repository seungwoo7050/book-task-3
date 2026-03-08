import { randomUUID } from "crypto";
import { Book, CreateBookDto, UpdateBookDto } from "../types";

/**
 * BookService — Business logic and in-memory data store.
 *
 * This class has NO knowledge of Express, HTTP, or request/response objects.
 * It works exclusively with plain TypeScript types.
 */
export class BookService {
  private readonly books = new Map<string, Book>();

  /** Return all books as an array. */
  findAll(): Book[] {
    return Array.from(this.books.values());
  }

  /** Find a single book by ID. Returns undefined if not found. */
  findById(id: string): Book | undefined {
    return this.books.get(id);
  }

  /** Create a new book with a generated UUID. */
  create(dto: CreateBookDto): Book {
    const book: Book = {
      id: randomUUID(),
      ...dto,
    };
    this.books.set(book.id, book);
    return book;
  }

  /** Update an existing book. Returns the updated book or undefined if not found. */
  update(id: string, dto: UpdateBookDto): Book | undefined {
    const existing = this.books.get(id);
    if (!existing) {
      return undefined;
    }
    const updated: Book = { ...existing, ...dto };
    this.books.set(id, updated);
    return updated;
  }

  /** Delete a book by ID. Returns true if deleted, false if not found. */
  delete(id: string): boolean {
    return this.books.delete(id);
  }
}
