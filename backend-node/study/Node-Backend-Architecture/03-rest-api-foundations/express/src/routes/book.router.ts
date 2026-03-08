import { Router } from "express";
import { BookController } from "../controllers/book.controller";
import { asyncHandler } from "../utils/async-handler";

/**
 * Creates and returns an Express Router for /books endpoints.
 *
 * This function receives a BookController instance (dependency injection)
 * and maps HTTP methods + paths to controller methods.
 *
 * No business logic lives here — only route definitions.
 */
export function createBookRouter(controller: BookController): Router {
  const router = Router();

  router.get("/", asyncHandler(controller.findAll));
  router.get("/:id", asyncHandler(controller.findById));
  router.post("/", asyncHandler(controller.create));
  router.put("/:id", asyncHandler(controller.update));
  router.delete("/:id", asyncHandler(controller.delete));

  return router;
}
