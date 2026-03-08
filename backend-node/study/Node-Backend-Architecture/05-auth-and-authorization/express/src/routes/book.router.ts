import { Router } from "express";
import { BookController } from "../controllers/book.controller";
import { authMiddleware } from "../middleware/auth.middleware";
import { requireRole } from "../middleware/role.middleware";
import { asyncHandler } from "../utils/async-handler";

export function createBookRouter(controller: BookController): Router {
  const router = Router();

  // Public routes
  router.get("/", asyncHandler(controller.findAll));
  router.get("/:id", asyncHandler(controller.findById));

  // Protected routes — require auth + ADMIN role
  router.post("/", authMiddleware, requireRole("ADMIN"), asyncHandler(controller.create));
  router.put("/:id", authMiddleware, requireRole("ADMIN"), asyncHandler(controller.update));
  router.delete("/:id", authMiddleware, requireRole("ADMIN"), asyncHandler(controller.delete));

  return router;
}
