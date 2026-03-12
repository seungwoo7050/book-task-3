import crypto from "node:crypto";
import { Book } from "../types/book";
import { NotFoundError } from "../errors";
import { BookRepository } from "../repositories/book.repository";
import { CreateBookDto, UpdateBookDto } from "../schemas/book.schema";

export class BookService {
  constructor(private readonly bookRepository: BookRepository) {}

  findAll(): Book[] {
    return this.bookRepository.findAll();
  }

  findById(id: string): Book {
    const book = this.bookRepository.findById(id);
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
    return this.bookRepository.create(book);
  }

  update(id: string, dto: UpdateBookDto): Book {
    const updated = this.bookRepository.update(id, dto);
    if (!updated) {
      throw new NotFoundError(`Book with id '${id}' not found`);
    }
    return updated;
  }

  delete(id: string): void {
    const deleted = this.bookRepository.delete(id);
    if (!deleted) {
      throw new NotFoundError(`Book with id '${id}' not found`);
    }
  }
}
