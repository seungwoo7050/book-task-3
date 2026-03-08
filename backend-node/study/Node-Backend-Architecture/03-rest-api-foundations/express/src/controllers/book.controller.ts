import { Request, Response } from "express";
import { BookService } from "../services/book.service";

/**
 * BookController — Translates HTTP requests into service calls and sends responses.
 *
 * Receives BookService via constructor injection (manual DI).
 * Each method extracts data from req, calls the service, and sends an HTTP response.
 */
export class BookController {
  constructor(private readonly bookService: BookService) {
    // Bind all handler methods to preserve `this` context when passed as callbacks
    this.findAll = this.findAll.bind(this);
    this.findById = this.findById.bind(this);
    this.create = this.create.bind(this);
    this.update = this.update.bind(this);
    this.delete = this.delete.bind(this);
  }

  /** GET /books — List all books. */
  async findAll(_req: Request, res: Response): Promise<void> {
    const books = this.bookService.findAll();
    res.json(books);
  }

  /** GET /books/:id — Get a single book. */
  async findById(req: Request, res: Response): Promise<void> {
    const id = Array.isArray(req.params.id) ? req.params.id[0] : req.params.id;
    const book = this.bookService.findById(id);
    if (!book) {
      res.status(404).json({ error: "Book not found" });
      return;
    }
    res.json(book);
  }

  /** POST /books — Create a new book. */
  async create(req: Request, res: Response): Promise<void> {
    const book = this.bookService.create(req.body);
    res.status(201).json(book);
  }

  /** PUT /books/:id — Update an existing book. */
  async update(req: Request, res: Response): Promise<void> {
    const id = Array.isArray(req.params.id) ? req.params.id[0] : req.params.id;
    const book = this.bookService.update(id, req.body);
    if (!book) {
      res.status(404).json({ error: "Book not found" });
      return;
    }
    res.json(book);
  }

  /** DELETE /books/:id — Delete a book. */
  async delete(req: Request, res: Response): Promise<void> {
    const id = Array.isArray(req.params.id) ? req.params.id[0] : req.params.id;
    const deleted = this.bookService.delete(id);
    if (!deleted) {
      res.status(404).json({ error: "Book not found" });
      return;
    }
    res.status(204).send();
  }
}
