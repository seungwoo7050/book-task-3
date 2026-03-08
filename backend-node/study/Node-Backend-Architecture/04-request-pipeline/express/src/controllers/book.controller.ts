import { Request, Response } from "express";
import { BookService } from "../services/book.service";

export class BookController {
  constructor(private readonly bookService: BookService) {
    this.findAll = this.findAll.bind(this);
    this.findById = this.findById.bind(this);
    this.create = this.create.bind(this);
    this.update = this.update.bind(this);
    this.delete = this.delete.bind(this);
  }

  async findAll(_req: Request, res: Response): Promise<void> {
    const books = this.bookService.findAll();
    res.json(books);
  }

  async findById(req: Request, res: Response): Promise<void> {
    const id = Array.isArray(req.params.id) ? req.params.id[0] : req.params.id;
    const book = this.bookService.findById(id);
    res.json(book);
  }

  async create(req: Request, res: Response): Promise<void> {
    const book = this.bookService.create(req.body);
    res.status(201).json(book);
  }

  async update(req: Request, res: Response): Promise<void> {
    const id = Array.isArray(req.params.id) ? req.params.id[0] : req.params.id;
    const book = this.bookService.update(id, req.body);
    res.json(book);
  }

  async delete(req: Request, res: Response): Promise<void> {
    const id = Array.isArray(req.params.id) ? req.params.id[0] : req.params.id;
    this.bookService.delete(id);
    res.status(204).send();
  }
}
