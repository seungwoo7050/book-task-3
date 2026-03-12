# Express vs NestJS: Side-by-Side Comparison

This document compares the Express implementation (Assignment 1-A) with the NestJS implementation (Assignment 1-B) to highlight the architectural differences.

## Project Structure

### Express
```
src/
├── main.ts
├── app.ts
├── types/book.ts
├── services/book.service.ts
├── controllers/book.controller.ts
├── routes/book.router.ts
└── utils/async-handler.ts
```

### NestJS
```
src/
├── main.ts
├── app.module.ts
└── books/
    ├── books.module.ts
    ├── books.controller.ts
    ├── books.service.ts
    ├── dto/
    │   ├── create-book.dto.ts
    │   └── update-book.dto.ts
    └── entities/
        └── book.entity.ts
```

**Key difference**: NestJS organizes code by **feature** (books/) rather than by **technical role** (controllers/, services/).

## Route Definition

### Express
```typescript
// book.router.ts
const router = Router();
router.get("/", asyncHandler(controller.findAll));
router.get("/:id", asyncHandler(controller.findById));
router.post("/", asyncHandler(controller.create));

// app.ts
app.use("/books", bookRouter);
```

### NestJS
```typescript
// books.controller.ts
@Controller("books")
export class BooksController {
  @Get()
  findAll() { ... }

  @Get(":id")
  findOne(@Param("id") id: string) { ... }

  @Post()
  create(@Body() dto: CreateBookDto) { ... }
}
```

**Key difference**: No separate router file. Routes are declared inline with decorators.

## Dependency Injection

### Express (Manual)
```typescript
// app.ts — you are the DI container
const bookService = new BookService();
const bookController = new BookController(bookService);
const bookRouter = createBookRouter(bookController);
```

### NestJS (Automatic)
```typescript
// books.module.ts — framework is the DI container
@Module({
  controllers: [BooksController],
  providers: [BooksService],
})
export class BooksModule {}
```

**Key difference**: NestJS automatically creates instances and resolves constructor dependencies. You declare *what* to inject, not *how*.

## Error Handling

### Express
```typescript
// controller
async findById(req: Request, res: Response): Promise<void> {
  const book = this.bookService.findById(req.params.id);
  if (!book) {
    res.status(404).json({ error: "Book not found" });
    return;
  }
  res.json(book);
}
```

### NestJS
```typescript
// controller
@Get(":id")
findOne(@Param("id") id: string) {
  const book = this.booksService.findOne(id);
  if (!book) {
    throw new NotFoundException("Book not found");
  }
  return book;
}
```

**Key difference**: NestJS uses exception classes instead of manual `res.status().json()`. The framework handles serialization.

## Request/Response Handling

### Express
```typescript
async create(req: Request, res: Response): Promise<void> {
  const book = this.bookService.create(req.body);
  res.status(201).json(book);
}
```

### NestJS
```typescript
@Post()
@HttpCode(201) // 201 is default for @Post, so this is optional
create(@Body() dto: CreateBookDto) {
  return this.booksService.create(dto);
}
```

**Key difference**: In NestJS, you simply `return` the data — the framework serializes it to JSON and sets the Content-Type.

## `asyncHandler` — Where Did It Go?

In Express, you needed `asyncHandler` to catch async errors. In NestJS, this is handled automatically by the framework. Every controller method is wrapped in error handling internally.

## Summary Table

| Aspect            | Express                     | NestJS                        |
| ----------------- | --------------------------- | ----------------------------- |
| Router            | `express.Router()` + manual | `@Controller` + `@Get`/`@Post`|
| DI                | Manual wiring in `app.ts`   | Module `providers` array      |
| Error Handling    | `asyncHandler` + error MW   | Built-in exception filters    |
| Request Data      | `req.params`, `req.body`    | `@Param()`, `@Body()`        |
| Response          | `res.status().json()`       | `return value`               |
| Organization      | By role (controllers/)      | By feature (books/)           |
| Boilerplate       | More manual setup           | Convention + decorators        |

## 근거 요약

- 근거: [문서] `backend-architecture/01-rest-api/README.md`
- 근거: [문서] `backend-architecture/01-rest-api/lab-report.md`
- 근거: [문서] `backend-architecture/01-rest-api/nestjs-impl/docs/README.md`
- 근거: [문서] `backend-architecture/01-rest-api/nestjs-impl/devlog/README.md`
