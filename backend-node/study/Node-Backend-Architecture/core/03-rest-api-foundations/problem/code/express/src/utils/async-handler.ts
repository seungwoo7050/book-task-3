/**
 * asyncHandler - async route handler를 감싸는 유틸리티다.
 *
 * Express는 async handler에서 발생한 오류를 기본으로 잡지 못한다.
 * 이 wrapper는 reject된 promise를 잡아 next()로 전달한다.
 *
 * TODO: 이 유틸리티 함수를 구현한다.
 *
 * 사용 예:
 *   router.get("/", asyncHandler(async (req, res) => { ... }));
 */

import { Request, Response, NextFunction } from "express";

export function asyncHandler(
  fn: (req: Request, res: Response, next: NextFunction) => Promise<void>
) {
  // TODO: 오류를 잡아 next(err)를 호출하는 함수를 반환한다
  return fn; // placeholder
}
