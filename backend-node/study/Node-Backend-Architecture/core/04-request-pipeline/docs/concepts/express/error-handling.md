# Centralized Error Handling in Express

## The Problem

Without centralized error handling, every route handler needs its own try-catch:

```typescript
// ❌ Repetitive and inconsistent
router.get("/:id", async (req, res) => {
  try {
    const book = service.findById(req.params.id);
    if (!book) return res.status(404).json({ error: "Not found" });
    res.json(book);
  } catch (err) {
    res.status(500).json({ error: "Internal error" });
  }
});
```

## The Solution: Custom Error Classes + Global Handler

### 1. Define Error Hierarchy

```typescript
export class AppError extends Error {
  constructor(
    public readonly statusCode: number,
    message: string,
  ) {
    super(message);
    this.name = this.constructor.name;
  }
}

export class NotFoundError extends AppError {
  constructor(message = "Resource not found") {
    super(404, message);
  }
}

export class ValidationError extends AppError {
  constructor(message: string, public readonly details?: unknown) {
    super(400, message);
  }
}
```

### 2. Throw Errors in Services

```typescript
findById(id: string): Book {
  const book = this.books.get(id);
  if (!book) throw new NotFoundError(`Book ${id} not found`);
  return book;
}
```

### 3. Global Error Handler

```typescript
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  if (err instanceof AppError) {
    res.status(err.statusCode).json({
      success: false,
      error: { message: err.message, statusCode: err.statusCode },
    });
    return;
  }

  // Unknown error — log and return 500
  console.error("[Unhandled Error]", err);
  res.status(500).json({
    success: false,
    error: { message: "Internal Server Error", statusCode: 500 },
  });
});
```

This ensures **every error** produces a consistent JSON response.

## 근거 요약

- 근거: [문서] `backend-architecture/03-pipeline/README.md`
- 근거: [문서] `backend-architecture/03-pipeline/lab-report.md`
- 근거: [문서] `backend-architecture/03-pipeline/express-impl/docs/README.md`
- 근거: [문서] `backend-architecture/03-pipeline/express-impl/devlog/README.md`
