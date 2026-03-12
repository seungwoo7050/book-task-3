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

  async findAll(_req: Request, res: Response): Promise<void> { res.json(this.bookService.findAll()); }
  async findById(req: Request, res: Response): Promise<void> {
    const id = Array.isArray(req.params.id) ? req.params.id[0] : req.params.id;
    res.json(this.bookService.findById(id));
  }
  async create(req: Request, res: Response): Promise<void> { res.status(201).json(this.bookService.create(req.body)); }
  async update(req: Request, res: Response): Promise<void> {
    const id = Array.isArray(req.params.id) ? req.params.id[0] : req.params.id;
    res.json(this.bookService.update(id, req.body));
  }
  async delete(req: Request, res: Response): Promise<void> {
    const id = Array.isArray(req.params.id) ? req.params.id[0] : req.params.id;
    this.bookService.delete(id);
    res.status(204).send();
  }
}
