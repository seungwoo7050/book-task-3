import crypto from "node:crypto";
import { Book } from "../types/book";
import { NotFoundError } from "../errors";
import { CreateBookDto, UpdateBookDto } from "../schemas/book.schema";

export class BookService {
  private books: Map<string, Book> = new Map();

  findAll(): Book[] {
    return Array.from(this.books.values());
  }

  findById(id: string): Book {
    const book = this.books.get(id);
    if (!book) {
      throw new NotFoundError(`Book with id '${id}' not found`);
    }
    return book;
  }

  create(dto: CreateBookDto): Book {
    const now = new Date();
    const book: Book = {
      id: crypto.randomUUID(),
      ...dto,
      createdAt: now,
      updatedAt: now,
    };
    this.books.set(book.id, book);
    return book;
  }

  update(id: string, dto: UpdateBookDto): Book {
    const book = this.findById(id);
    const updated: Book = {
      ...book,
      ...dto,
      updatedAt: new Date(),
    };
    this.books.set(id, updated);
    return updated;
  }

  delete(id: string): void {
    const book = this.books.get(id);
    if (!book) {
      throw new NotFoundError(`Book with id '${id}' not found`);
    }
    this.books.delete(id);
  }
}
