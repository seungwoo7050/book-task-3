import { Request, Response, NextFunction } from "express";

/**
 * 성공 응답을 표준 envelope로 감싼다:
 * { success: true, data: <original body> }
 *
 * route handler가 실행되기 전에 res.json()을 덮어써 동작한다.
 */
export function responseWrapper(
  _req: Request,
  res: Response,
  next: NextFunction,
): void {
  const originalJson = res.json.bind(res);

  res.json = function (body?: unknown): Response {
    // body에 이미 `success` 필드가 있으면 그대로 통과시킨다(오류 응답).
    if (body && typeof body === "object" && "success" in (body as Record<string, unknown>)) {
      return originalJson(body);
    }
    return originalJson({ success: true, data: body });
  };

  next();
}
