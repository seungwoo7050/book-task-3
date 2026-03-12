import crypto from "node:crypto";
import { Book } from "../types/book";
import { NotFoundError } from "../errors";
import { BookRepository } from "../repositories/book.repository";
import { EventBus } from "../events/event-bus";
import { CreateBookDto, UpdateBookDto } from "../schemas/book.schema";

export class BookService {
  constructor(
    private readonly bookRepository: BookRepository,
    private readonly eventBus: EventBus,
  ) {}

  findAll(): Book[] {
    return this.bookRepository.findAll();
  }

  findById(id: string): Book {
    const book = this.bookRepository.findById(id);
    if (!book) throw new NotFoundError(`Book with id '${id}' not found`);
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
    const created = this.bookRepository.create(book);

    this.eventBus.emit("book.created", {
      bookId: created.id,
      title: created.title,
      author: created.author,
      timestamp: new Date(),
    });

    return created;
  }

  update(id: string, dto: UpdateBookDto): Book {
    const updated = this.bookRepository.update(id, dto);
    if (!updated) throw new NotFoundError(`Book with id '${id}' not found`);

    const changes = Object.keys(dto);
    this.eventBus.emit("book.updated", {
      bookId: id,
      changes,
      timestamp: new Date(),
    });

    return updated;
  }

  delete(id: string): void {
    const deleted = this.bookRepository.delete(id);
    if (!deleted) throw new NotFoundError(`Book with id '${id}' not found`);

    this.eventBus.emit("book.deleted", {
      bookId: id,
      timestamp: new Date(),
    });
  }
}
