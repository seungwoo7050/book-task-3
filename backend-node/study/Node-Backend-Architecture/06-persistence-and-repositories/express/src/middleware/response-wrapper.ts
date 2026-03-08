import { Request, Response, NextFunction } from "express";

export function responseWrapper(_req: Request, res: Response, next: NextFunction): void {
  const originalJson = res.json.bind(res);
  res.json = function (body?: unknown): Response {
    if (body && typeof body === "object" && "success" in (body as Record<string, unknown>)) {
      return originalJson(body);
    }
    return originalJson({ success: true, data: body });
  };
  next();
}
