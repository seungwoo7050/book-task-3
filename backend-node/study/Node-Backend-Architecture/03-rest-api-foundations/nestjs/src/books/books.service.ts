import { Injectable, NotFoundException } from "@nestjs/common";
import { randomUUID } from "crypto";
import { Book } from "./entities/book.entity";
import { CreateBookDto } from "./dto/create-book.dto";
import { UpdateBookDto } from "./dto/update-book.dto";

/**
 * BooksService — Business logic and in-memory data store.
 *
 * Decorated with @Injectable() so the NestJS DI container
 * can manage its lifecycle and inject it into controllers.
 */
@Injectable()
export class BooksService {
  private readonly books = new Map<string, Book>();

  findAll(): Book[] {
    return Array.from(this.books.values());
  }

  findOne(id: string): Book {
    const book = this.books.get(id);
    if (!book) {
      throw new NotFoundException(`Book with ID "${id}" not found`);
    }
    return book;
  }

  create(dto: CreateBookDto): Book {
    const book: Book = {
      id: randomUUID(),
      ...dto,
    };
    this.books.set(book.id, book);
    return book;
  }

  update(id: string, dto: UpdateBookDto): Book {
    const existing = this.books.get(id);
    if (!existing) {
      throw new NotFoundException(`Book with ID "${id}" not found`);
    }
    const updated: Book = { ...existing, ...dto };
    this.books.set(id, updated);
    return updated;
  }

  remove(id: string): void {
    const exists = this.books.has(id);
    if (!exists) {
      throw new NotFoundException(`Book with ID "${id}" not found`);
    }
    this.books.delete(id);
  }
}
