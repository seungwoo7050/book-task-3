export type BookRecord = {
  id: string;
  title: string;
  author: string;
  publishedYear: number;
};

export type CreateBookPayload = {
  title: string;
  author: string;
  publishedYear: number;
};

export class BookStore {
  private readonly books = new Map<string, BookRecord>();
  private nextId = 1;

  list(): BookRecord[] {
    return [...this.books.values()];
  }

  getById(id: string): BookRecord | undefined {
    return this.books.get(id);
  }

  create(payload: CreateBookPayload): BookRecord {
    const book: BookRecord = {
      id: String(this.nextId),
      title: payload.title,
      author: payload.author,
      publishedYear: payload.publishedYear,
    };

    this.books.set(book.id, book);
    this.nextId += 1;

    return book;
  }
}

export function validateCreateBookPayload(payload: unknown): CreateBookPayload {
  if (typeof payload !== "object" || payload === null) {
    throw new Error("Request body must be a JSON object");
  }

  const candidate = payload as Record<string, unknown>;
  const { title, author, publishedYear } = candidate;

  if (typeof title !== "string" || title.trim().length === 0) {
    throw new Error("title is required");
  }

  if (typeof author !== "string" || author.trim().length === 0) {
    throw new Error("author is required");
  }

  if (typeof publishedYear !== "number" || !Number.isInteger(publishedYear)) {
    throw new Error("publishedYear must be an integer");
  }

  return {
    title: title.trim(),
    author: author.trim(),
    publishedYear,
  };
}
