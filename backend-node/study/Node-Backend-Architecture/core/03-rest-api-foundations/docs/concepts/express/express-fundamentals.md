# Express.js Fundamentals

## What is Express?

Express is a **minimal, unopinionated web framework** for Node.js. It provides a thin layer of fundamental web application features on top of Node's built-in `http` module, without obscuring the underlying platform.

Key characteristics:
- **Middleware-driven** — Everything is a middleware function.
- **Routing** — Maps HTTP method + URL path to handler functions.
- **Unopinionated** — No enforced project structure or patterns.

## The Request–Response Cycle

Every Express application follows the same flow:

```
Client Request
    ↓
[Middleware Stack]  →  express.json()  →  cors()  →  ...
    ↓
[Route Matching]   →  router.get("/books", handler)
    ↓
[Handler Function] →  (req, res, next) => { ... }
    ↓
Client Response
```

### The `(req, res, next)` Signature

Every middleware and route handler receives three arguments:

| Argument | Type              | Purpose                                                   |
| -------- | ----------------- | --------------------------------------------------------- |
| `req`    | `Request`         | Incoming HTTP request (headers, body, params, query, etc.)|
| `res`    | `Response`        | Outgoing HTTP response (status, headers, body)            |
| `next`   | `NextFunction`    | Passes control to the next middleware in the stack         |

```typescript
import { Request, Response, NextFunction } from "express";

function logger(req: Request, res: Response, next: NextFunction): void {
  console.log(`${req.method} ${req.url}`);
  next(); // MUST call next() or the request hangs
}
```

## Middleware

Middleware functions execute **in the order they are registered**. Each middleware can:

1. Execute any code.
2. Modify `req` and `res` objects.
3. End the request–response cycle by calling `res.send()`, `res.json()`, etc.
4. Call `next()` to pass control to the next middleware.

### Types of Middleware

```typescript
// Application-level middleware
app.use(express.json());

// Route-level middleware
router.use(authMiddleware);

// Error-handling middleware (4 arguments)
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error(err.stack);
  res.status(500).json({ error: "Internal Server Error" });
});
```

### Important: Error-Handling Middleware

Express identifies error-handling middleware by its **four-parameter signature**. This must always be registered **last** in the middleware chain:

```typescript
// This MUST have exactly 4 parameters to be recognized as error middleware
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  res.status(500).json({ message: err.message });
});
```

## Routing

### Express Router

`express.Router()` creates a modular, mountable route handler. Think of it as a "mini-application" that only handles routing.

```typescript
import { Router } from "express";

const router = Router();

router.get("/",    (req, res) => { /* list */   });
router.get("/:id", (req, res) => { /* get one */ });
router.post("/",   (req, res) => { /* create */  });
router.put("/:id", (req, res) => { /* update */  });
router.delete("/:id", (req, res) => { /* delete */ });

export default router;
```

### Mounting a Router

```typescript
import express from "express";
import bookRouter from "./routes/book.router";

const app = express();
app.use("/books", bookRouter); // All routes prefixed with /books
```

### Route Parameters

```typescript
// URL: GET /books/abc-123
router.get("/:id", (req, res) => {
  const bookId = req.params.id; // "abc-123"
});
```

## The `asyncHandler` Pattern

Express does **not** catch errors thrown inside `async` route handlers. If an `async` handler throws, the error is silently swallowed and the request hangs.

**Problem:**
```typescript
// ❌ If findAll() rejects, Express never sees the error
router.get("/", async (req, res) => {
  const books = await service.findAll();
  res.json(books);
});
```

**Solution — asyncHandler wrapper:**
```typescript
function asyncHandler(
  fn: (req: Request, res: Response, next: NextFunction) => Promise<void>
) {
  return (req: Request, res: Response, next: NextFunction) => {
    fn(req, res, next).catch(next);
  };
}

// ✅ Errors are now forwarded to Express error middleware
router.get("/", asyncHandler(async (req, res) => {
  const books = await service.findAll();
  res.json(books);
}));
```

## JSON Body Parsing

Express does not parse JSON request bodies by default. You must add the `express.json()` middleware:

```typescript
const app = express();
app.use(express.json()); // Parses JSON bodies into req.body
```

Without this, `req.body` will be `undefined` for POST and PUT requests.

## 근거 요약

- 근거: [문서] `backend-architecture/01-rest-api/README.md`
- 근거: [문서] `backend-architecture/01-rest-api/lab-report.md`
- 근거: [문서] `backend-architecture/01-rest-api/express-impl/docs/README.md`
- 근거: [문서] `backend-architecture/01-rest-api/express-impl/devlog/README.md`
