import { Injectable, Inject, NotFoundException } from "@nestjs/common";
import { InjectRepository } from "@nestjs/typeorm";
import { EventEmitter2 } from "@nestjs/event-emitter";
import { Repository } from "typeorm";
import { randomUUID } from "node:crypto";
import { Book } from "./entities/book.entity";
import { CreateBookDto } from "./dto/create-book.dto";
import { UpdateBookDto } from "./dto/update-book.dto";
import { BookCreatedEvent, BookUpdatedEvent, BookDeletedEvent } from "../events/events";
import { RedisService } from "../runtime/redis.service";
import { RuntimeConfigService } from "../runtime/runtime-config.service";

@Injectable()
export class BooksService {
  private readonly listCacheKey = "books:list";

  constructor(
    @InjectRepository(Book)
    private readonly bookRepository: Repository<Book>,
    @Inject(EventEmitter2)
    private readonly eventEmitter: EventEmitter2,
    @Inject(RedisService)
    private readonly redisService: RedisService,
    @Inject(RuntimeConfigService)
    private readonly runtimeConfig: RuntimeConfigService,
  ) {}

  async findAll(): Promise<Book[]> {
    const cached = await this.redisService.getJson<Book[]>(this.listCacheKey);
    if (cached) {
      return cached;
    }

    const books = await this.bookRepository.find({ order: { createdAt: "DESC" } });
    await this.redisService.setJson(
      this.listCacheKey,
      books,
      this.runtimeConfig.booksCacheTtlSeconds,
    );
    return books;
  }

  async findOne(id: string): Promise<Book> {
    const detailCacheKey = this.getDetailCacheKey(id);
    const cached = await this.redisService.getJson<Book>(detailCacheKey);
    if (cached) {
      return cached;
    }

    const book = await this.bookRepository.findOneBy({ id });
    if (!book) {
      throw new NotFoundException(`Book with id '${id}' not found`);
    }
    await this.redisService.setJson(detailCacheKey, book, this.runtimeConfig.booksCacheTtlSeconds);
    return book;
  }

  async create(dto: CreateBookDto): Promise<Book> {
    const book = this.bookRepository.create({
      id: randomUUID(),
      ...dto,
    });
    const saved = await this.bookRepository.save(book);

    this.eventEmitter.emit(
      "book.created",
      new BookCreatedEvent(saved.id, saved.title, saved.author),
    );
    await this.invalidateBookCaches(saved.id);

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
    await this.invalidateBookCaches(saved.id);

    return saved;
  }

  async remove(id: string): Promise<void> {
    const book = await this.findOne(id);
    await this.bookRepository.remove(book);

    this.eventEmitter.emit(
      "book.deleted",
      new BookDeletedEvent(id),
    );
    await this.invalidateBookCaches(id);
  }

  private async invalidateBookCaches(id: string): Promise<void> {
    await this.redisService.deleteMany([this.listCacheKey, this.getDetailCacheKey(id)]);
  }

  private getDetailCacheKey(id: string): string {
    return `books:detail:${id}`;
  }
}
