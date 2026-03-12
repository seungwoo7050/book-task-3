import { randomUUID } from "crypto";
import { Book, CreateBookDto, UpdateBookDto } from "../types";

/**
 * BookService - 비즈니스 로직과 in-memory 저장소를 담당한다.
 *
 * 이 클래스는 Express, HTTP, request/response 객체를 알지 못한다.
 * 순수 TypeScript 타입만 사용한다.
 */
export class BookService {
  private readonly books = new Map<string, Book>();

  /** 전체 책을 배열로 반환한다. */
  findAll(): Book[] {
    return Array.from(this.books.values());
  }

  /** ID로 단일 책을 찾는다. 없으면 undefined를 반환한다. */
  findById(id: string): Book | undefined {
    return this.books.get(id);
  }

  /** 생성 a new book with a generated UUID. */
  create(dto: CreateBookDto): Book {
    const book: Book = {
      id: randomUUID(),
      ...dto,
    };
    this.books.set(book.id, book);
    return book;
  }

  /** 수정 an existing book. Returns the updated book or undefined if not found. */
  update(id: string, dto: UpdateBookDto): Book | undefined {
    const existing = this.books.get(id);
    if (!existing) {
      return undefined;
    }
    const updated: Book = { ...existing, ...dto };
    this.books.set(id, updated);
    return updated;
  }

  /** ID로 책을 삭제한다. 삭제되면 true, 없으면 false를 반환한다. */
  delete(id: string): boolean {
    return this.books.delete(id);
  }
}
