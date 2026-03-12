import { describe, it, expect, beforeEach, vi } from "vitest";
import { Test } from "@nestjs/testing";
import { getRepositoryToken } from "@nestjs/typeorm";
import { EventEmitter2 } from "@nestjs/event-emitter";
import { NotFoundException } from "@nestjs/common";
import { BooksService } from "../../src/books/books.service";
import { Book } from "../../src/books/entities/book.entity";
import { BookCreatedEvent, BookUpdatedEvent, BookDeletedEvent } from "../../src/events/events";
import { RedisService } from "../../src/runtime/redis.service";
import { RuntimeConfigService } from "../../src/runtime/runtime-config.service";

const mockBook: Book = {
  id: "book-id",
  title: "Clean Code",
  author: "Robert C. Martin",
  publishedYear: 2008,
  genre: "Programming",
  price: 33.99,
  createdAt: new Date(),
  updatedAt: new Date(),
};

describe("BooksService", () => {
  let service: BooksService;
  let mockEmitter: { emit: ReturnType<typeof vi.fn> };
  let mockRepository: Record<string, ReturnType<typeof vi.fn>>;
  let mockRedisService: Record<string, ReturnType<typeof vi.fn>>;
  let mockRuntimeConfig: { booksCacheTtlSeconds: number };

  beforeEach(async () => {
    mockEmitter = { emit: vi.fn() };
    mockRedisService = {
      getJson: vi.fn().mockResolvedValue(null),
      setJson: vi.fn().mockResolvedValue(undefined),
      deleteMany: vi.fn().mockResolvedValue(undefined),
    };
    mockRuntimeConfig = {
      booksCacheTtlSeconds: 30,
    };
    mockRepository = {
      find: vi.fn().mockResolvedValue([mockBook]),
      findOneBy: vi.fn().mockResolvedValue(mockBook),
      create: vi.fn().mockReturnValue(mockBook),
      save: vi.fn().mockResolvedValue(mockBook),
      remove: vi.fn().mockResolvedValue(undefined),
    };

    const module = await Test.createTestingModule({
      providers: [
        BooksService,
        { provide: getRepositoryToken(Book), useValue: mockRepository },
        { provide: EventEmitter2, useValue: mockEmitter },
        { provide: RedisService, useValue: mockRedisService },
        { provide: RuntimeConfigService, useValue: mockRuntimeConfig },
      ],
    }).compile();

    service = module.get(BooksService);
  });

  it("should create a book and emit event", async () => {
    const result = await service.create({
      title: "Clean Code",
      author: "Robert C. Martin",
      publishedYear: 2008,
      genre: "Programming",
      price: 33.99,
    });

    expect(result.title).toBe("Clean Code");
    expect(mockEmitter.emit).toHaveBeenCalledWith("book.created", expect.any(BookCreatedEvent));
    expect(mockRedisService.deleteMany).toHaveBeenCalledWith(["books:list", "books:detail:book-id"]);
  });

  it("should update a book and emit event", async () => {
    const result = await service.update("book-id", { price: 29.99 });

    expect(result).toBeDefined();
    expect(mockEmitter.emit).toHaveBeenCalledWith("book.updated", expect.any(BookUpdatedEvent));
    expect(mockRedisService.deleteMany).toHaveBeenCalledWith(["books:list", "books:detail:book-id"]);
  });

  it("should delete a book and emit event", async () => {
    await service.remove("book-id");

    expect(mockEmitter.emit).toHaveBeenCalledWith("book.deleted", expect.any(BookDeletedEvent));
    expect(mockRedisService.deleteMany).toHaveBeenCalledWith(["books:list", "books:detail:book-id"]);
  });

  it("should throw NotFoundException for missing book", async () => {
    mockRepository.findOneBy.mockResolvedValue(null);

    await expect(service.findOne("missing")).rejects.toThrow(NotFoundException);
    expect(mockEmitter.emit).not.toHaveBeenCalled();
  });

  it("should return all books", async () => {
    const result = await service.findAll();

    expect(result).toHaveLength(1);
    expect(mockRepository.find).toHaveBeenCalled();
    expect(mockRedisService.setJson).toHaveBeenCalledWith("books:list", [mockBook], 30);
  });

  it("should return cached books without querying the repository", async () => {
    mockRedisService.getJson.mockResolvedValueOnce([mockBook]);

    const result = await service.findAll();

    expect(result).toEqual([mockBook]);
    expect(mockRepository.find).not.toHaveBeenCalled();
  });
});
