import { describe, it, expect, beforeEach, vi } from "vitest";
import { Test } from "@nestjs/testing";
import { getRepositoryToken } from "@nestjs/typeorm";
import { EventEmitter2 } from "@nestjs/event-emitter";
import { NotFoundException } from "@nestjs/common";
import { BooksService } from "../../src/books/books.service";
import { Book } from "../../src/books/entities/book.entity";
import { BookCreatedEvent, BookUpdatedEvent, BookDeletedEvent } from "../../src/events/events";

const mockBook: Book = {
  id: "test-id",
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

  beforeEach(async () => {
    mockEmitter = { emit: vi.fn() };
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
      ],
    }).compile();

    service = module.get(BooksService);
  });

  it("should emit book.created event after creating a book", async () => {
    await service.create({
      title: "Clean Code",
      author: "Robert C. Martin",
      publishedYear: 2008,
      genre: "Programming",
      price: 33.99,
    });

    expect(mockEmitter.emit).toHaveBeenCalledWith(
      "book.created",
      expect.any(BookCreatedEvent),
    );
    const event = mockEmitter.emit.mock.calls[0][1] as BookCreatedEvent;
    expect(event.title).toBe("Clean Code");
    expect(event.author).toBe("Robert C. Martin");
  });

  it("should emit book.updated event after updating a book", async () => {
    await service.update("test-id", { price: 29.99 });

    expect(mockEmitter.emit).toHaveBeenCalledWith(
      "book.updated",
      expect.any(BookUpdatedEvent),
    );
    const event = mockEmitter.emit.mock.calls[0][1] as BookUpdatedEvent;
    expect(event.bookId).toBe("test-id");
    expect(event.changes).toContain("price");
  });

  it("should emit book.deleted event after removing a book", async () => {
    await service.remove("test-id");

    expect(mockEmitter.emit).toHaveBeenCalledWith(
      "book.deleted",
      expect.any(BookDeletedEvent),
    );
    const event = mockEmitter.emit.mock.calls[0][1] as BookDeletedEvent;
    expect(event.bookId).toBe("test-id");
  });

  it("should not emit events when book is not found", async () => {
    mockRepository.findOneBy.mockResolvedValue(null);

    await expect(service.update("nonexistent", { price: 10 })).rejects.toThrow(
      NotFoundException,
    );
    expect(mockEmitter.emit).not.toHaveBeenCalled();
  });

  it("should return all books", async () => {
    const books = await service.findAll();
    expect(books).toHaveLength(1);
    expect(mockRepository.find).toHaveBeenCalled();
  });
});
