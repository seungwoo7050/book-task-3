import { Router } from "express";
import { BookController } from "../controllers/book.controller";
import { BookService } from "../services/book.service";
import { BookRepository } from "../repositories/book.repository";
import { validate } from "../middleware/validate";
import { CreateBookSchema, UpdateBookSchema } from "../schemas/book.schema";
import { asyncHandler } from "../utils/async-handler";
import Database from "better-sqlite3";

export function createBookRouter(db: Database.Database): Router {
  const repository = new BookRepository(db);
  const service = new BookService(repository);
  const controller = new BookController(service);
  const router = Router();

  router.get("/", asyncHandler(controller.findAll));
  router.get("/:id", asyncHandler(controller.findById));
  router.post("/", validate(CreateBookSchema), asyncHandler(controller.create));
  router.put("/:id", validate(UpdateBookSchema), asyncHandler(controller.update));
  router.delete("/:id", asyncHandler(controller.delete));

  return router;
}
