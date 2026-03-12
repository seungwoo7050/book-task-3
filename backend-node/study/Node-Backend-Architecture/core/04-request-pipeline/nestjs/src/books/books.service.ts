import { Injectable, NotFoundException } from "@nestjs/common";
import crypto from "node:crypto";
import { Book } from "./entities/book.entity";
import { CreateBookDto } from "./dto/create-book.dto";
import { UpdateBookDto } from "./dto/update-book.dto";

@Injectable()
export class BooksService {
  private books: Map<string, Book> = new Map();

  findAll(): Book[] {
    return Array.from(this.books.values());
  }

  findOne(id: string): Book {
    const book = this.books.get(id);
    if (!book) {
      throw new NotFoundException(`Book with id '${id}' not found`);
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
    const book = this.findOne(id);
    const updated: Book = {
      ...book,
      ...dto,
      updatedAt: new Date(),
    };
    this.books.set(id, updated);
    return updated;
  }

  remove(id: string): void {
    const book = this.books.get(id);
    if (!book) {
      throw new NotFoundException(`Book with id '${id}' not found`);
    }
    this.books.delete(id);
  }
}
