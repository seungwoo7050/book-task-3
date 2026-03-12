import { Router } from "express";
import { BookController } from "../controllers/book.controller";
import { authmiddleware } from "../middleware/auth.middleware";
import { requireRole } from "../middleware/role.middleware";
import { asyncHandler } from "../utils/async-handler";

export function createBookRouter(controller: BookController): Router {
  const router = Router();

  // 공개 라우트
  router.get("/", asyncHandler(controller.findAll));
  router.get("/:id", asyncHandler(controller.findById));

  // 보호된 라우트 - auth + ADMIN role이 필요하다
  router.post("/", authmiddleware, requireRole("ADMIN"), asyncHandler(controller.create));
  router.put("/:id", authmiddleware, requireRole("ADMIN"), asyncHandler(controller.update));
  router.delete("/:id", authmiddleware, requireRole("ADMIN"), asyncHandler(controller.delete));

  return router;
}
