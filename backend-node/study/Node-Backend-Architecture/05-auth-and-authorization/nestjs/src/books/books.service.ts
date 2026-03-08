import { Injectable, NotFoundException } from "@nestjs/common";
import { randomUUID } from "crypto";
import type { Book } from "./entities/book.entity";

@Injectable()
export class BooksService {
  private readonly books = new Map<string, Book>();

  findAll(): Book[] {
    return Array.from(this.books.values());
  }

  findOne(id: string): Book {
    const book = this.books.get(id);
    if (!book) throw new NotFoundException(`Book with ID "${id}" not found`);
    return book;
  }

  create(dto: Omit<Book, "id">): Book {
    const book: Book = { id: randomUUID(), ...dto };
    this.books.set(book.id, book);
    return book;
  }

  update(id: string, dto: Partial<Omit<Book, "id">>): Book {
    const existing = this.books.get(id);
    if (!existing) throw new NotFoundException(`Book with ID "${id}" not found`);
    const updated = { ...existing, ...dto };
    this.books.set(id, updated);
    return updated;
  }

  remove(id: string): void {
    if (!this.books.has(id)) throw new NotFoundException(`Book with ID "${id}" not found`);
    this.books.delete(id);
  }
}
