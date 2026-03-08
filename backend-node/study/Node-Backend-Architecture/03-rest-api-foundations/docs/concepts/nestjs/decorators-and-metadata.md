# Decorators and Metadata in NestJS

## TypeScript Decorators

Decorators are **special functions** that attach metadata to classes, methods, or parameters. They are a Stage 3 ECMAScript proposal, enabled in TypeScript via `experimentalDecorators`.

```json
// tsconfig.json
{
  "compilerOptions": {
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true
  }
}
```

### Decorator Types

| Type       | Syntax              | Purpose                           |
| ---------- | -------------------- | -------------------------------- |
| Class      | `@Module()`          | Attach metadata to a class       |
| Method     | `@Get()`             | Attach metadata to a method      |
| Parameter  | `@Body()`            | Attach metadata to a parameter   |
| Property   | `@Inject()`          | Attach metadata to a property    |

### How `@Controller("books")` Works

When you write:
```typescript
@Controller("books")
export class BooksController { ... }
```

NestJS stores the string `"books"` as metadata on the `BooksController` class using `Reflect.defineMetadata()`. At startup, the framework reads this metadata to register routes with the prefix `/books`.

### How `@Get(":id")` Works

```typescript
@Get(":id")
findOne(@Param("id") id: string) { ... }
```

This stores metadata on the `findOne` method:
- HTTP method: `GET`
- Path: `:id`
- Parameter index 0 → extract from `req.params.id`

At startup, NestJS reads all this metadata and calls `router.get("/books/:id", handler)` on the underlying Express app — exactly what you did manually in Assignment 1-A.

## `emitDecoratorMetadata`

When `emitDecoratorMetadata` is enabled, TypeScript emits type information at runtime. This is how NestJS knows **what to inject** via constructors:

```typescript
@Injectable()
export class BooksController {
  constructor(private readonly booksService: BooksService) {}
}
```

At compile time, TypeScript emits metadata that says: "The first constructor parameter is of type `BooksService`." The DI container reads this metadata to resolve the correct provider.

## From Manual to Automated

| Express (Manual)                     | NestJS (Decorators)               |
| ------------------------------------ | --------------------------------- |
| `router.get("/", handler)`           | `@Get()`                          |
| `router.get("/:id", handler)`        | `@Get(":id")`                     |
| `req.params.id`                      | `@Param("id") id: string`        |
| `req.body`                           | `@Body() dto: CreateBookDto`     |
| `new BookController(bookService)`    | DI container auto-resolves        |
| `app.use("/books", router)`          | `@Controller("books")`           |

The decorator approach is more **declarative** — you describe *what* you want, and the framework handles *how*.

## 근거 요약

- 근거: [문서] `backend-architecture/01-rest-api/README.md`
- 근거: [문서] `backend-architecture/01-rest-api/lab-report.md`
- 근거: [문서] `backend-architecture/01-rest-api/nestjs-impl/docs/README.md`
- 근거: [문서] `backend-architecture/01-rest-api/nestjs-impl/devlog/README.md`
