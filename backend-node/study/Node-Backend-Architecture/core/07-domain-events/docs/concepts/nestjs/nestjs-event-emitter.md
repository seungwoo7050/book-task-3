# @nestjs/event-emitter

## Overview

`@nestjs/event-emitter` is an official NestJS package that integrates `eventemitter2` into the NestJS ecosystem. It provides decorator-based event listeners and seamless DI integration.

## Installation

```bash
pnpm add @nestjs/event-emitter
```

## Module Registration

Register `EventEmitterModule` at the root of your application:

```typescript
import { Module } from "@nestjs/common";
import { EventEmitterModule } from "@nestjs/event-emitter";

@Module({
  imports: [
    EventEmitterModule.forRoot(),
  ],
})
export class AppModule {}
```

### Configuration Options

```typescript
EventEmitterModule.forRoot({
  wildcard: false,          // Enable wildcard listeners
  delimiter: ".",           // Delimiter for namespaced events
  maxListeners: 10,         // Max listeners per event
  verboseMemoryLeak: true,  // Warn on memory leaks
})
```

## Emitting Events

Inject `EventEmitter2` into any service and call `emit()`:

```typescript
import { Injectable } from "@nestjs/common";
import { EventEmitter2 } from "@nestjs/event-emitter";

@Injectable()
export class BooksService {
  constructor(private readonly eventEmitter: EventEmitter2) {}

  async create(dto: CreateBookDto): Promise<Book> {
    const book = await this.bookRepository.save(/* ... */);

    this.eventEmitter.emit("book.created", new BookCreatedEvent(book.id, book.title));

    return book;
  }
}
```

### Key Points

- `emit(event: string, ...values: any[])` — synchronous emission
- `emitAsync(event: string, ...values: any[])` — waits for all async handlers
- Events are dispatched **after** the business logic completes
- The return value of `emit` is `boolean` (true if any handler was called)

## Listening to Events

### @OnEvent Decorator

Use `@OnEvent()` on any method of an `@Injectable()` provider:

```typescript
import { Injectable } from "@nestjs/common";
import { OnEvent } from "@nestjs/event-emitter";

@Injectable()
export class BookEventListener {
  @OnEvent("book.created")
  handleBookCreated(event: BookCreatedEvent): void {
    console.log(`[Event] Book created: ${event.title}`);
  }

  @OnEvent("book.updated")
  handleBookUpdated(event: BookUpdatedEvent): void {
    console.log(`[Event] Book updated: ${event.bookId}`);
  }
}
```

### Decorator Options

```typescript
@OnEvent("book.created", {
  async: true,        // Handle asynchronously
  prependListener: false,
  suppressErrors: false,
})
```

### Wildcard Listeners

When `wildcard: true` is enabled in the module config:

```typescript
@OnEvent("book.*")
handleAllBookEvents(event: unknown): void {
  console.log("Some book event happened");
}
```

## Event Classes

Define event payload as plain classes:

```typescript
export class BookCreatedEvent {
  constructor(
    public readonly bookId: string,
    public readonly title: string,
    public readonly author: string,
    public readonly timestamp: Date = new Date(),
  ) {}
}

export class BookUpdatedEvent {
  constructor(
    public readonly bookId: string,
    public readonly changes: string[],
    public readonly timestamp: Date = new Date(),
  ) {}
}

export class BookDeletedEvent {
  constructor(
    public readonly bookId: string,
    public readonly timestamp: Date = new Date(),
  ) {}
}
```

Using classes (vs. plain objects) enables:
- Type checking at the listener level
- Potential use with `class-transformer` for serialization
- Clean constructors with default values

## Module Structure

The listener must be registered as a provider in a module:

```typescript
@Module({
  providers: [BookEventListener],
})
export class EventsModule {}
```

Or directly in the same module as the service:

```typescript
@Module({
  imports: [TypeOrmModule.forFeature([Book])],
  controllers: [BooksController],
  providers: [BooksService, BookEventListener],
})
export class BooksModule {}
```

## Error Handling in Listeners

By default, if a listener throws, the error propagates to the emitter. To prevent this, wrap listener logic in try-catch:

```typescript
@OnEvent("book.created")
handleBookCreated(event: BookCreatedEvent): void {
  try {
    // side-effect logic (logging, notifications, etc.)
  } catch (error) {
    console.error("Listener error:", error);
  }
}
```

Alternatively, use `suppressErrors: true` in `@OnEvent()` options (available in eventemitter2):

```typescript
@OnEvent("book.created", { suppressErrors: true })
```

## Testing

### Unit Testing

Mock `EventEmitter2` to verify event emission:

```typescript
const mockEmitter = { emit: vi.fn() };

const module = await Test.createTestingModule({
  providers: [
    BooksService,
    { provide: EventEmitter2, useValue: mockEmitter },
  ],
}).compile();

// After calling service method:
expect(mockEmitter.emit).toHaveBeenCalledWith("book.created", expect.any(BookCreatedEvent));
```

### E2E Testing

Use a complete NestJS application with `EventEmitterModule`:

```typescript
const module = await Test.createTestingModule({
  imports: [AppModule],
}).compile();

const app = module.createNestApplication();
await app.init();

// Make HTTP request and check side effects
```

## Comparison with Express EventEmitter

| Feature                    | Node.js EventEmitter         | @nestjs/event-emitter       |
|----------------------------|------------------------------|------------------------------|
| Registration               | Manual `.on()`               | `@OnEvent()` decorator       |
| DI Integration             | Manual wiring                | Automatic via providers      |
| Type Safety                | Requires wrapper (EventBus)  | Event class + decorator      |
| Wildcard Support           | No                           | Yes (via eventemitter2)      |
| Async Emission             | No                           | `emitAsync()` supported      |
| Error Suppression          | Manual try-catch             | `suppressErrors` option      |

## 근거 요약

- 근거: [문서] `backend-architecture/05-event-system/README.md`
- 근거: [문서] `backend-architecture/05-event-system/lab-report.md`
- 근거: [문서] `backend-architecture/05-event-system/nestjs-impl/docs/README.md`
- 근거: [문서] `backend-architecture/05-event-system/nestjs-impl/devlog/README.md`
