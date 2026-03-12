# Dependency Injection in Plain TypeScript

## What is Dependency Injection?

**Dependency Injection (DI)** is a design pattern where an object receives its dependencies from the outside rather than creating them internally.

### Without DI (tight coupling)

```typescript
class BookController {
  private service = new BookService(); // ❌ Creates its own dependency
}
```

**Problems:**
- `BookController` is permanently coupled to `BookService`.
- You cannot substitute a mock service for testing.
- If `BookService` requires constructor arguments, `BookController` must know about them.

### With DI (loose coupling)

```typescript
class BookController {
  constructor(private readonly service: BookService) {} // ✅ Receives dependency
}
```

**Benefits:**
- `BookController` does not know how `BookService` is created.
- You can inject a mock for testing.
- Changing the service implementation does not require changing the controller.

## The Composition Root

When using manual DI, all object creation and wiring happens in one place called the **composition root**. In Express, this is typically your `app.ts` or `main.ts` file.

```typescript
// src/main.ts — The Composition Root

// 1. Create leaf dependencies first (no dependencies of their own)
const bookService = new BookService();

// 2. Create objects that depend on the leaves
const bookController = new BookController(bookService);

// 3. Create objects that depend on the above
const bookRouter = createBookRouter(bookController);

// 4. Assemble the application
app.use("/books", bookRouter);
```

### Key Principle: Dependencies Flow Inward

```
main.ts → creates → Service
main.ts → creates → Controller(Service)
main.ts → creates → Router(Controller)
main.ts → mounts  → Router on Express app
```

The composition root is the **only place** that knows about all concrete classes. Every other file only knows about the interfaces it directly uses.

## Constructor Injection Pattern

The most common form of DI is **constructor injection**: dependencies are passed as constructor parameters.

```typescript
export class BookController {
  // TypeScript shorthand: declares AND assigns private readonly property
  constructor(private readonly bookService: BookService) {}

  async findAll(req: Request, res: Response): Promise<void> {
    const books = this.bookService.findAll();
    res.json(books);
  }
}
```

The `private readonly` parameter shorthand is equivalent to:

```typescript
export class BookController {
  private readonly bookService: BookService;

  constructor(bookService: BookService) {
    this.bookService = bookService;
  }
}
```

## Testing Advantage

With DI, unit testing becomes straightforward because you can inject mocks:

```typescript
// In a test file
const mockService = {
  findAll: () => [{ id: "1", title: "Test Book", author: "Test Author" }],
  findById: (id: string) => undefined,
  create: (data: any) => ({ id: "1", ...data }),
};

const controller = new BookController(mockService as any);
// Now you can test controller behavior without a real service
```

## From Manual DI to Automated DI

In this assignment, you wire dependencies manually. The code works perfectly, but as the application grows, the composition root becomes increasingly complex:

```typescript
// Imagine 20 services, 20 controllers, 20 routers...
const userService = new UserService();
const authService = new AuthService(userService);
const bookService = new BookService();
const orderService = new OrderService(bookService, userService);
const paymentService = new PaymentService(orderService);
// ... this grows quickly
```

This is **exactly the problem** that NestJS's DI container solves. In Assignment 1-B (NestJS), you will see how the `@Injectable()` decorator and module system automate this entire wiring process.

## Summary

| Concept           | In This Assignment          | In NestJS                     |
| ----------------- | --------------------------- | ----------------------------- |
| DI Method         | Constructor parameters      | `@Injectable()` + constructor |
| Wiring Location   | `main.ts` (manual)          | Module `providers` (auto)     |
| Service Discovery | Explicit `new Service()`    | Automatic by DI container     |
| Scope             | Singleton (one instance)    | Configurable (singleton/request/transient) |

## 근거 요약

- 근거: [문서] `backend-architecture/01-rest-api/README.md`
- 근거: [문서] `backend-architecture/01-rest-api/lab-report.md`
- 근거: [문서] `backend-architecture/01-rest-api/express-impl/docs/README.md`
- 근거: [문서] `backend-architecture/01-rest-api/express-impl/devlog/README.md`
