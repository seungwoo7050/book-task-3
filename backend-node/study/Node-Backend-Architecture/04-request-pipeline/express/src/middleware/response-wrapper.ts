import { Request, Response, NextFunction } from "express";

/**
 * Wraps successful responses in a standard envelope:
 * { success: true, data: <original body> }
 *
 * Works by overriding res.json() before the route handler executes.
 */
export function responseWrapper(
  _req: Request,
  res: Response,
  next: NextFunction,
): void {
  const originalJson = res.json.bind(res);

  res.json = function (body?: unknown): Response {
    // If the body already has a `success` field, pass through (error responses)
    if (body && typeof body === "object" && "success" in (body as Record<string, unknown>)) {
      return originalJson(body);
    }
    return originalJson({ success: true, data: body });
  };

  next();
}
