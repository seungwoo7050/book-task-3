# Layered Architecture: Router → Controller → Service

## Why Layers?

In a small Express application, you might put everything in one file: route definitions, request handling, data access, and business logic. This works for prototypes but becomes **unmaintainable** as the application grows.

The **layered architecture** pattern separates code by **responsibility**, making it easier to:

- **Read** — Each file has a single purpose.
- **Test** — Each layer can be tested in isolation.
- **Refactor** — Changing one layer does not cascade into others.
- **Scale** — Multiple developers can work on different layers simultaneously.

## The Three Layers

```
┌─────────────────────────────────────────────┐
│  HTTP Layer (Express)                       │
│  ┌──────────────────────────────────────┐   │
│  │  Router                              │   │
│  │  - Defines routes (method + path)    │   │
│  │  - Delegates to Controller           │   │
│  └──────────┬───────────────────────────┘   │
│             │                               │
│  ┌──────────▼───────────────────────────┐   │
│  │  Controller                          │   │
│  │  - Extracts data from req            │   │
│  │  - Calls Service methods             │   │
│  │  - Sends HTTP responses via res      │   │
│  └──────────┬───────────────────────────┘   │
│             │                               │
└─────────────┼───────────────────────────────┘
              │
┌─────────────▼───────────────────────────────┐
│  Business Layer                             │
│  ┌──────────────────────────────────────┐   │
│  │  Service                             │   │
│  │  - Business logic                    │   │
│  │  - Data access (CRUD operations)     │   │
│  │  - No knowledge of HTTP/Express      │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

## Router: The Traffic Director

The Router's **only job** is to map incoming HTTP requests to the correct Controller method.

**Rules:**
- NO business logic.
- NO data transformation.
- NO direct `req.body` or `req.params` usage — pass the whole handler.

```typescript
// src/routes/book.router.ts
import { Router } from "express";
import { BookController } from "../controllers/book.controller";
import { asyncHandler } from "../utils/async-handler";

export function createBookRouter(controller: BookController): Router {
  const router = Router();

  router.get("/",    asyncHandler(controller.findAll));
  router.get("/:id", asyncHandler(controller.findById));
  router.post("/",   asyncHandler(controller.create));

  return router;
}
```

## Controller: The Translator

The Controller **translates** between the HTTP world (`req`/`res`) and the business world (plain TypeScript types).

**Rules:**
- Extracts data from `req` (params, body, query, headers).
- Calls Service layer methods with **typed arguments**.
- Sends HTTP responses with proper status codes.
- Does NOT implement business logic (validation logic, computation, etc. belong in the Service).

```typescript
// src/controllers/book.controller.ts
import { Request, Response } from "express";
import { BookService } from "../services/book.service";

export class BookController {
  constructor(private readonly bookService: BookService) {
    // Bind methods to preserve `this` context
    this.findAll = this.findAll.bind(this);
    this.findById = this.findById.bind(this);
    this.create = this.create.bind(this);
  }

  async findAll(req: Request, res: Response): Promise<void> {
    const books = this.bookService.findAll();
    res.json(books);
  }

  async findById(req: Request, res: Response): Promise<void> {
    const book = this.bookService.findById(req.params.id);
    if (!book) {
      res.status(404).json({ error: "Book not found" });
      return;
    }
    res.json(book);
  }

  async create(req: Request, res: Response): Promise<void> {
    const newBook = this.bookService.create(req.body);
    res.status(201).json(newBook);
  }
}
```

### Why `bind(this)`?

When you pass a class method as a callback (e.g., `router.get("/", controller.findAll)`), the `this` context is lost. Binding in the constructor ensures `this` always refers to the class instance.

## Service: The Brain

The Service contains **all business logic**. It is completely independent of the HTTP layer.

**Rules:**
- NO imports from Express.
- NO knowledge of `req` or `res`.
- Works with plain TypeScript types.
- Can be reused in CLI tools, WebSocket handlers, tests, etc.

```typescript
// src/services/book.service.ts
import { randomUUID } from "crypto";

interface Book {
  id: string;
  title: string;
  author: string;
}

export class BookService {
  private books = new Map<string, Book>();

  findAll(): Book[] {
    return Array.from(this.books.values());
  }

  findById(id: string): Book | undefined {
    return this.books.get(id);
  }

  create(data: Omit<Book, "id">): Book {
    const book: Book = { id: randomUUID(), ...data };
    this.books.set(book.id, book);
    return book;
  }
}
```

## Wiring It All Together

All layers are connected in a single file — the **composition root**:

```typescript
// src/app.ts
import express from "express";
import { BookService } from "./services/book.service";
import { BookController } from "./controllers/book.controller";
import { createBookRouter } from "./routes/book.router";

const app = express();
app.use(express.json());

// Manual Dependency Injection
const bookService = new BookService();
const bookController = new BookController(bookService);
const bookRouter = createBookRouter(bookController);

app.use("/books", bookRouter);

export default app;
```

This is **Manual Dependency Injection** — you are the DI container. In NestJS, a real DI container automates this wiring process.

## 근거 요약

- 근거: [문서] `backend-architecture/01-rest-api/README.md`
- 근거: [문서] `backend-architecture/01-rest-api/lab-report.md`
- 근거: [문서] `backend-architecture/01-rest-api/express-impl/docs/README.md`
- 근거: [문서] `backend-architecture/01-rest-api/express-impl/devlog/README.md`
