import { randomUUID } from "crypto";
import { Book, CreateBookDto, UpdateBookDto } from "../types";

export class BookService {
  private readonly books = new Map<string, Book>();

  findAll(): Book[] {
    return Array.from(this.books.values());
  }

  findById(id: string): Book | undefined {
    return this.books.get(id);
  }

  create(dto: CreateBookDto): Book {
    const book: Book = { id: randomUUID(), ...dto };
    this.books.set(book.id, book);
    return book;
  }

  update(id: string, dto: UpdateBookDto): Book | undefined {
    const existing = this.books.get(id);
    if (!existing) return undefined;
    const updated: Book = { ...existing, ...dto };
    this.books.set(id, updated);
    return updated;
  }

  delete(id: string): boolean {
    return this.books.delete(id);
  }
}
