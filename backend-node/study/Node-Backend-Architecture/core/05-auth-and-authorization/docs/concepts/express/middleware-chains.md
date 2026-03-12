# Middleware Chains for Authentication

## The Chain Pattern

Express processes middleware **in order of registration**. For auth, this creates a natural pipeline:

```
Request → [authMiddleware] → [roleMiddleware] → [Controller Handler] → Response
```

If any middleware calls `res.status().json()` instead of `next()`, the chain stops.

## Auth Middleware

```typescript
function authMiddleware(req: Request, res: Response, next: NextFunction): void {
  // 1. Extract token
  const token = extractToken(req.headers.authorization);
  if (!token) {
    res.status(401).json({ error: "Authentication required" });
    return;
  }

  // 2. Verify token
  try {
    const decoded = jwt.verify(token, SECRET);
    req.user = decoded; // 3. Attach to request
    next();             // 4. Pass to next middleware
  } catch {
    res.status(401).json({ error: "Invalid token" });
  }
}
```

## Role Middleware Factory

A **factory function** returns middleware configured for specific roles:

```typescript
function requireRole(...allowedRoles: string[]) {
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
```

Usage:
```typescript
router.post("/books", authMiddleware, requireRole("ADMIN"), controller.create);
```

## Extending the Request Type

TypeScript does not know about `req.user`. Extend the Express `Request` interface:

```typescript
// src/types/express.d.ts
declare namespace Express {
  interface Request {
    user?: {
      sub: string;
      username: string;
      role: string;
    };
  }
}
```

## Middleware Order Matters

```typescript
// ✅ Correct: auth first, then role check
router.post("/", authMiddleware, requireRole("ADMIN"), controller.create);

// ❌ Wrong: role check before auth — req.user is undefined
router.post("/", requireRole("ADMIN"), authMiddleware, controller.create);
```

The auth middleware MUST run before the role middleware because `requireRole` reads `req.user`, which is set by `authMiddleware`.

## 근거 요약

- 근거: [문서] `backend-architecture/02-auth-guards/README.md`
- 근거: [문서] `backend-architecture/02-auth-guards/lab-report.md`
- 근거: [문서] `backend-architecture/02-auth-guards/express-impl/docs/README.md`
- 근거: [문서] `backend-architecture/02-auth-guards/express-impl/devlog/README.md`
