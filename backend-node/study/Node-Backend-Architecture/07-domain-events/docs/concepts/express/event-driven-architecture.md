# Event-Driven Architecture

## Concept

In Event-Driven Architecture (EDA), components communicate through **events** rather than direct method calls. A component emits an event when something interesting happens, and other components listen for and react to those events.

## Domain Events

Domain events represent something that happened in the business domain:

```
BookCreated  → A new book was added to the catalog
BookUpdated  → A book's information was changed
BookDeleted  → A book was removed from the catalog
```

## Benefits

1. **Loose Coupling** — The emitter doesn't know about listeners
2. **Open/Closed Principle** — Add new reactions without modifying existing code
3. **Side Effect Separation** — Core logic stays clean; side effects live in listeners
4. **Extensibility** — Add audit logging, notifications, cache invalidation as separate listeners

## Synchronous vs Asynchronous Events

### Synchronous (in-process)
```
Service.create() → emit("book.created") → Listener runs immediately → return
```
All listeners complete before the service method returns.

### Asynchronous (message queue)
```
Service.create() → publish to queue → return immediately
                                      → Worker processes later
```

In this chapter, we use **synchronous in-process events** via EventEmitter.

## Event Structure

Events should be immutable data objects:

```typescript
interface BookCreatedEvent {
  readonly bookId: string;
  readonly title: string;
  readonly timestamp: Date;
}
```

## 근거 요약

- 근거: [문서] `backend-architecture/05-event-system/README.md`
- 근거: [문서] `backend-architecture/05-event-system/lab-report.md`
- 근거: [문서] `backend-architecture/05-event-system/express-impl/docs/README.md`
- 근거: [문서] `backend-architecture/05-event-system/express-impl/devlog/README.md`
