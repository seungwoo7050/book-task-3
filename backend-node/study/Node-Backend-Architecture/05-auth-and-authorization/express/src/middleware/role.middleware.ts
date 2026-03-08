import { Request, Response, NextFunction } from "express";

/**
 * Role middleware factory — returns middleware that checks if the
 * authenticated user has one of the allowed roles.
 *
 * Must be used AFTER authMiddleware (req.user must exist).
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
