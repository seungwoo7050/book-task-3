/**
 * Book Router - 라우트 정의만 담당한다.
 *
 * TODO:
 *   1. Express Router를 생성한다.
 *   2. HTTP method + path를 BookController 메서드에 연결한다.
 *   3. 각 handler를 asyncHandler로 감싼다.
 *   4. 여기에는 비즈니스 로직을 두지 않고 라우팅만 둔다.
 */

import { Router } from "express";

export function createBookRouter(/* TODO: accept controller */): Router {
  const router = Router();

  // TODO: 라우트를 정의한다
  // router.get("/", ...)
  // router.get("/:id", ...)
  // router.post("/", ...)
  // router.put("/:id", ...)
  // router.delete("/:id", ...)

  return router;
}
