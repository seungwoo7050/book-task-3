# Domain Events in NestJS

## What are Domain Events?

Domain events represent something meaningful that happened in the business domain. They are named in past tense and carry relevant data about the occurrence.

```
book.created  → A new book was added to the catalog
book.updated  → An existing book's information was changed
book.deleted  → A book was removed from the catalog
```

## Event-Driven Architecture Benefits

### 1. Loose Coupling

Without events:
```typescript
// BooksService is coupled to NotificationService, AuditService, CacheService...
async create(dto: CreateBookDto): Promise<Book> {
  const book = await this.bookRepository.save(newBook);
  await this.notificationService.notify(book);
  await this.auditService.log("create", book);
  this.cacheService.invalidate("books");
  return book;
}
```

With events:
```typescript
// BooksService only knows about EventEmitter2
async create(dto: CreateBookDto): Promise<Book> {
  const book = await this.bookRepository.save(newBook);
  this.eventEmitter.emit("book.created", new BookCreatedEvent(book.id, book.title, book.author));
  return book;
}
```

### 2. Open-Closed Principle

Adding new side effects requires only adding new listeners, not modifying existing services.

### 3. Separation of Concerns

Core business logic (CRUD) is separated from side effects (logging, notifications, caching).

## Event Lifecycle in NestJS

```
HTTP Request
  → Controller
    → Service.create()
      → Repository.save()        (core logic)
      → eventEmitter.emit()      (fire-and-forget)
        → @OnEvent listener 1    (logging)
        → @OnEvent listener 2    (notifications)
        → @OnEvent listener N    (any side effect)
    ← Response returned to client
```

## Design Guidelines

### Event Naming Convention

Use `resource.action` pattern with dot notation:

```
book.created
book.updated
book.deleted
user.registered
order.placed
```

### Event Payload Design

Include just enough data for listeners to act:

```typescript
// Good: Minimal but sufficient
export class BookCreatedEvent {
  constructor(
    public readonly bookId: string,
    public readonly title: string,
    public readonly author: string,
    public readonly timestamp: Date = new Date(),
  ) {}
}

// Bad: Entire entity (over-sharing, tight coupling)
export class BookCreatedEvent {
  constructor(public readonly book: Book) {}
}
```

### Emit After Success

Always emit events **after** the core operation succeeds:

```typescript
async create(dto: CreateBookDto): Promise<Book> {
  // 1. Core logic first
  const book = await this.bookRepository.save(newBook);

  // 2. Emit event only after success
  this.eventEmitter.emit("book.created", new BookCreatedEvent(...));

  return book;
}
```

### Listener Error Isolation

Listeners should never break the main flow:

```typescript
@OnEvent("book.created")
handleBookCreated(event: BookCreatedEvent): void {
  try {
    // Side effect that might fail
    console.log(`Book created: ${event.title}`);
  } catch (error) {
    // Log but don't re-throw
    console.error("Listener failed:", error);
  }
}
```

## Testing Event-Driven Code

### Testing the Emitter (Service)

Mock EventEmitter2 and verify `emit()` was called:

```typescript
expect(mockEmitter.emit).toHaveBeenCalledWith(
  "book.created",
  expect.objectContaining({ bookId: "123", title: "Test" }),
);
```

### Testing the Listener

Call the listener method directly with a test event:

```typescript
const listener = new BookEventListener();
const consoleSpy = vi.spyOn(console, "log");

listener.handleBookCreated(new BookCreatedEvent("1", "Test", "Author"));

expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining("Test"));
```

### Testing Integration

Use a full NestJS TestingModule with real EventEmitterModule to verify end-to-end flow.

## 근거 요약

- 근거: [문서] `backend-architecture/05-event-system/README.md`
- 근거: [문서] `backend-architecture/05-event-system/lab-report.md`
- 근거: [문서] `backend-architecture/05-event-system/nestjs-impl/docs/README.md`
- 근거: [문서] `backend-architecture/05-event-system/nestjs-impl/devlog/README.md`
