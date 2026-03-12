import { Request, Response, NextFunction } from "express";

/**
 * Role middleware factory - 다음 조건을 확인하는 middleware를 반환한다.
 * 인증된 사용자가 허용된 role 중 하나를 가졌는지 확인한다.
 *
 * authMiddleware 뒤에서 사용해야 한다(req.user가 있어야 한다).
 */
export function requireRole(...allowedRoles: string[]) {
  return (req: Request, res: Response, next: NextFunction): void => {
    if (!req.user) {
      res.status(401).json({ error: "Authentication required" });
      return;
    }

    if (!allowedRoles.includes(req.user.role)) {
      res.status(403).json({ error: "Insufficient permissions" });
      return;
    }

    next();
  };
}
