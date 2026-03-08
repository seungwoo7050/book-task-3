# Repository Pattern

## Definition

The **Repository Pattern** abstracts data access behind a collection-like interface. The application logic (Service) interacts with domain objects through the Repository, without knowing HOW or WHERE data is stored.

## Structure

```
Controller → Service → Repository → Database
```

- **Service**: Business logic, throws domain errors
- **Repository**: Data access, translates between domain objects and database rows

## Interface

```typescript
interface BookRepository {
  findAll(): Book[];
  findById(id: string): Book | null;
  create(book: Book): Book;
  update(id: string, data: Partial<Book>): Book | null;
  delete(id: string): boolean;
}
```

## Benefits

1. **Testability** — Swap real repository with in-memory stub for tests
2. **Separation of Concerns** — Service doesn't know about SQL
3. **Flexibility** — Switch from SQLite to PostgreSQL by changing only the repository
4. **Encapsulation** — SQL details stay in one place

## Column Mapping

Database columns use `snake_case`, while TypeScript uses `camelCase`:

```typescript
private toBook(row: BookRow): Book {
  return {
    id: row.id,
    title: row.title,
    author: row.author,
    publishedYear: row.published_year,
    genre: row.genre,
    price: row.price,
    createdAt: new Date(row.created_at),
    updatedAt: new Date(row.updated_at),
  };
}
```

## 근거 요약

- 근거: [문서] `backend-architecture/04-database/README.md`
- 근거: [문서] `backend-architecture/04-database/lab-report.md`
- 근거: [문서] `backend-architecture/04-database/express-impl/docs/README.md`
- 근거: [문서] `backend-architecture/04-database/express-impl/devlog/README.md`
