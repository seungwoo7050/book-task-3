import { Router } from "express";
import { BookController } from "../controllers/book.controller";
import { asyncHandler } from "../utils/async-handler";

/**
 * /books endpoint용 Express Router를 만들고 반환한다.
 *
 * 이 함수는 BookController 인스턴스(dependency injection)를 받아
 * HTTP method + path를 controller 메서드에 연결한다.
 *
 * 여기에는 비즈니스 로직을 두지 않고 route 정의만 둔다.
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
