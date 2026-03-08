import Database from "better-sqlite3";
import { Book, BookRow } from "../types/book";

export class BookRepository {
  constructor(private readonly db: Database.Database) {}

  findAll(): Book[] {
    const rows = this.db.prepare("SELECT * FROM books ORDER BY created_at DESC").all() as BookRow[];
    return rows.map(this.toBook);
  }

  findById(id: string): Book | null {
    const row = this.db.prepare("SELECT * FROM books WHERE id = ?").get(id) as BookRow | undefined;
    return row ? this.toBook(row) : null;
  }

  create(book: Book): Book {
    this.db.prepare(
      `INSERT INTO books (id, title, author, published_year, genre, price, created_at, updated_at)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?)`
    ).run(book.id, book.title, book.author, book.publishedYear, book.genre, book.price, book.createdAt.toISOString(), book.updatedAt.toISOString());
    return book;
  }

  update(id: string, data: Partial<Book>): Book | null {
    const existing = this.findById(id);
    if (!existing) return null;
    const updated: Book = { ...existing, ...data, updatedAt: new Date() };
    this.db.prepare(
      `UPDATE books SET title = ?, author = ?, published_year = ?, genre = ?, price = ?, updated_at = ? WHERE id = ?`
    ).run(updated.title, updated.author, updated.publishedYear, updated.genre, updated.price, updated.updatedAt.toISOString(), id);
    return updated;
  }

  delete(id: string): boolean {
    const result = this.db.prepare("DELETE FROM books WHERE id = ?").run(id);
    return result.changes > 0;
  }

  private toBook(row: BookRow): Book {
    return {
      id: row.id, title: row.title, author: row.author,
      publishedYear: row.published_year, genre: row.genre, price: row.price,
      createdAt: new Date(row.created_at), updatedAt: new Date(row.updated_at),
    };
  }
}
