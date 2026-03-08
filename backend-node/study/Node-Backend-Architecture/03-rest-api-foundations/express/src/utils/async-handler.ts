import { Request, Response, NextFunction } from "express";

/**
 * Wraps an async Express route handler to catch rejected promises
 * and forward them to Express error-handling middleware via next().
 */
export function asyncHandler(
  fn: (req: Request, res: Response, next: NextFunction) => Promise<void>
) {
  return (req: Request, res: Response, next: NextFunction): void => {
    fn(req, res, next).catch(next);
  };
}
