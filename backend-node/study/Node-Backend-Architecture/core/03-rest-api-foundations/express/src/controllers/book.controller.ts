import { Request, Response } from "express";
import { BookService } from "../services/book.service";

/**
 * BookController - HTTP 요청을 service 호출로 바꾸고 응답을 보낸다.
 *
 * constructor injection(수동 DI)으로 BookService를 받는다.
 * 각 메서드는 req에서 데이터를 꺼내 service를 호출하고 HTTP 응답을 보낸다.
 */
export class BookController {
  constructor(private readonly bookService: BookService) {
    // callback으로 넘길 때 `this` context를 유지하도록 handler를 bind한다.
    this.findAll = this.findAll.bind(this);
    this.findById = this.findById.bind(this);
    this.create = this.create.bind(this);
    this.update = this.update.bind(this);
    this.delete = this.delete.bind(this);
  }

  /** GET /books - 전체 책 목록을 조회한다. */
  async findAll(_req: Request, res: Response): Promise<void> {
    const books = this.bookService.findAll();
    res.json(books);
  }

  /** GET /books/:id - 단일 책을 조회한다. */
  async findById(req: Request, res: Response): Promise<void> {
    const id = Array.isArray(req.params.id) ? req.params.id[0] : req.params.id;
    const book = this.bookService.findById(id);
    if (!book) {
      res.status(404).json({ error: "Book not found" });
      return;
    }
    res.json(book);
  }

  /** POST /books — 생성 a new book. */
  async create(req: Request, res: Response): Promise<void> {
    const book = this.bookService.create(req.body);
    res.status(201).json(book);
  }

  /** PUT /books/:id — 수정 an existing book. */
  async update(req: Request, res: Response): Promise<void> {
    const id = Array.isArray(req.params.id) ? req.params.id[0] : req.params.id;
    const book = this.bookService.update(id, req.body);
    if (!book) {
      res.status(404).json({ error: "Book not found" });
      return;
    }
    res.json(book);
  }

  /** DELETE /books/:id - 책을 삭제한다. */
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
