import { Router } from "express";
import { BookController } from "../controllers/book.controller";
import { BookService } from "../services/book.service";
import { validate } from "../middleware/validate";
import { CreateBookSchema, UpdateBookSchema } from "../schemas/book.schema";
import { asyncHandler } from "../utils/async-handler";

export function createBookRouter(bookService?: BookService): Router {
  const service = bookService ?? new BookService();
  const controller = new BookController(service);
  const router = Router();

  router.get("/", asyncHandler(controller.findAll));
  router.get("/:id", asyncHandler(controller.findById));
  router.post("/", validate(CreateBookSchema), asyncHandler(controller.create));
  router.put("/:id", validate(UpdateBookSchema), asyncHandler(controller.update));
  router.delete("/:id", asyncHandler(controller.delete));

  return router;
}
