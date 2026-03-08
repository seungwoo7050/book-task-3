# Node.js EventEmitter

## Basics

`EventEmitter` is Node.js's built-in implementation of the Observer pattern:

```typescript
import { EventEmitter } from "node:events";

const emitter = new EventEmitter();

// Register listener
emitter.on("greet", (name: string) => {
  console.log(`Hello, ${name}!`);
});

// Emit event
emitter.emit("greet", "World");
```

## Typed EventBus

For type safety, we can create a typed wrapper:

```typescript
type EventMap = {
  "book.created": BookCreatedEvent;
  "book.updated": BookUpdatedEvent;
  "book.deleted": BookDeletedEvent;
};

class EventBus {
  private emitter = new EventEmitter();

  emit<K extends keyof EventMap>(event: K, data: EventMap[K]): void {
    this.emitter.emit(event, data);
  }

  on<K extends keyof EventMap>(event: K, handler: (data: EventMap[K]) => void): void {
    this.emitter.on(event, handler);
  }
}
```

## Error Handling in Listeners

If a listener throws, it can crash the process. Always wrap listener logic:

```typescript
emitter.on("book.created", (event) => {
  try {
    // side effect logic
  } catch (err) {
    console.error("Listener error:", err);
    // Don't re-throw — don't affect the main flow
  }
});
```

## Key Methods

| Method          | Description                              |
|----------------|------------------------------------------|
| `on(event, fn)` | Register a listener                     |
| `once(event, fn)` | Register a one-time listener          |
| `emit(event, ...args)` | Trigger all listeners for event  |
| `off(event, fn)` | Remove a specific listener             |
| `removeAllListeners(event?)` | Remove all listeners          |

## 근거 요약

- 근거: [문서] `backend-architecture/05-event-system/README.md`
- 근거: [문서] `backend-architecture/05-event-system/lab-report.md`
- 근거: [문서] `backend-architecture/05-event-system/express-impl/docs/README.md`
- 근거: [문서] `backend-architecture/05-event-system/express-impl/devlog/README.md`
