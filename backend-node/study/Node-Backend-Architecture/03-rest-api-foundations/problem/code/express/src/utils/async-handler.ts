/**
 * asyncHandler — Utility to wrap async route handlers.
 *
 * Express does not natively catch errors from async handlers.
 * This wrapper catches rejected promises and forwards them to next().
 *
 * TODO: Implement this utility function.
 *
 * Usage:
 *   router.get("/", asyncHandler(async (req, res) => { ... }));
 */

import { Request, Response, NextFunction } from "express";

export function asyncHandler(
  fn: (req: Request, res: Response, next: NextFunction) => Promise<void>
) {
  // TODO: Return a function that catches errors and calls next(err)
  return fn; // placeholder
}
