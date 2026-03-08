# Zod Validation in Express

## What is Zod?

Zod is a **TypeScript-first schema declaration and validation library**. Unlike `joi`, Zod schemas directly infer TypeScript types, giving you both runtime validation and compile-time type safety.

## Defining Schemas

```typescript
import { z } from "zod";

const CreateBookSchema = z.object({
  title: z.string().min(1, "Title is required"),
  author: z.string().min(1, "Author is required"),
  publishedYear: z.number().int().min(1000).max(2100),
  genre: z.string().min(1),
  price: z.number().positive("Price must be positive"),
});

// Infer the TypeScript type from the schema
type CreateBookDto = z.infer<typeof CreateBookSchema>;
```

## Validation Middleware Factory

```typescript
import { Request, Response, NextFunction } from "express";
import { ZodSchema, ZodError } from "zod";

function validate(schema: ZodSchema) {
  return (req: Request, res: Response, next: NextFunction): void => {
    try {
      req.body = schema.parse(req.body); // Also transforms/coerces
      next();
    } catch (err) {
      if (err instanceof ZodError) {
        res.status(400).json({
          success: false,
          error: {
            message: "Validation failed",
            details: err.errors.map(e => ({
              field: e.path.join("."),
              message: e.message,
            })),
          },
        });
        return;
      }
      next(err);
    }
  };
}
```

## Usage in Routes

```typescript
router.post("/", validate(CreateBookSchema), asyncHandler(controller.create));
router.put("/:id", validate(UpdateBookSchema), asyncHandler(controller.update));
```

The validation middleware runs BEFORE the controller, ensuring `req.body` is always valid.

## 근거 요약

- 근거: [문서] `backend-architecture/03-pipeline/README.md`
- 근거: [문서] `backend-architecture/03-pipeline/lab-report.md`
- 근거: [문서] `backend-architecture/03-pipeline/express-impl/docs/README.md`
- 근거: [문서] `backend-architecture/03-pipeline/express-impl/devlog/README.md`
