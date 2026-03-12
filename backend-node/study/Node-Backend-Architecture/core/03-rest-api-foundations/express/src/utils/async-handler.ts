import { Request, Response, NextFunction } from "express";

/**
 * reject된 promise를 잡기 위해 async Express route handler를 감싼다
 * 그리고 next()를 통해 Express 오류 처리 middleware로 전달한다.
 */
export function asyncHandler(
  fn: (req: Request, res: Response, next: NextFunction) => Promise<void>
) {
  return (req: Request, res: Response, next: NextFunction): void => {
    fn(req, res, next).catch(next);
  };
}
