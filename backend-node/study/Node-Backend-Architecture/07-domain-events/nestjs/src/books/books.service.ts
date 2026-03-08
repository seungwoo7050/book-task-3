import { Injectable, Inject, NotFoundException } from "@nestjs/common";
import { InjectRepository } from "@nestjs/typeorm";
import { EventEmitter2 } from "@nestjs/event-emitter";
import { Repository } from "typeorm";
import crypto from "node:crypto";
import { Book } from "./entities/book.entity";
import { CreateBookDto } from "./dto/create-book.dto";
import { UpdateBookDto } from "./dto/update-book.dto";
import { BookCreatedEvent, BookUpdatedEvent, BookDeletedEvent } from "../events/events";

@Injectable()
export class BooksService {
  constructor(
    @InjectRepository(Book)
    private readonly bookRepository: Repository<Book>,
    @Inject(EventEmitter2)
    private readonly eventEmitter: EventEmitter2,
  ) {}

  async findAll(): Promise<Book[]> {
    return this.bookRepository.find({ order: { createdAt: "DESC" } });
  }

  async findOne(id: string): Promise<Book> {
    const book = await this.bookRepository.findOneBy({ id });
    if (!book) {
      throw new NotFoundException(`Book with id '${id}' not found`);
    }
    return book;
  }

  async create(dto: CreateBookDto): Promise<Book> {
    const book = this.bookRepository.create({
      id: crypto.randomUUID(),
      ...dto,
    });
    const saved = await this.bookRepository.save(book);

    this.eventEmitter.emit(
      "book.created",
      new BookCreatedEvent(saved.id, saved.title, saved.author),
    );

    return saved;
  }

  async update(id: string, dto: UpdateBookDto): Promise<Book> {
    const book = await this.findOne(id);
    const changes = Object.keys(dto).filter(
      (key) => dto[key as keyof UpdateBookDto] !== undefined,
    );
    Object.assign(book, dto);
    const saved = await this.bookRepository.save(book);

    this.eventEmitter.emit(
      "book.updated",
      new BookUpdatedEvent(saved.id, changes),
    );

    return saved;
  }

  async remove(id: string): Promise<void> {
    const book = await this.findOne(id);
    await this.bookRepository.remove(book);

    this.eventEmitter.emit(
      "book.deleted",
      new BookDeletedEvent(id),
    );
  }
}
