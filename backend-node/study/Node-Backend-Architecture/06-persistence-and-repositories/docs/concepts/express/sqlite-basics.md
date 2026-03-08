# SQLite & better-sqlite3

## Why SQLite?

SQLite is a serverless, file-based relational database. Ideal for learning and prototyping:
- No separate server process
- Single file for the entire database
- Full SQL support (DDL, DML, transactions)

## better-sqlite3

`better-sqlite3` is a synchronous SQLite3 driver for Node.js:

```typescript
import Database from "better-sqlite3";

const db = new Database("bookstore.db");
// or in-memory:
const db = new Database(":memory:");
```

### Prepared Statements

```typescript
const stmt = db.prepare("SELECT * FROM books WHERE id = ?");
const book = stmt.get(id); // single row
const books = stmt.all();  // all rows
```

### Insert / Update / Delete

```typescript
const insert = db.prepare(
  "INSERT INTO books (id, title, author) VALUES (?, ?, ?)"
);
const info = insert.run(id, title, author);
// info.changes = number of rows affected
```

### Transactions

```typescript
const transfer = db.transaction(() => {
  insert.run(...);
  update.run(...);
});
transfer(); // All or nothing
```

## Synchronous API

Unlike `sqlite3` (callback-based) or `sql.js` (WASM), `better-sqlite3` is **synchronous**. This means:
- No callbacks or promises needed
- Simpler code flow
- Thread-safe within a single Node.js process
- Excellent performance (fastest SQLite driver for Node.js)

## Schema Initialization

```typescript
function initDatabase(db: Database.Database): void {
  db.exec(`
    CREATE TABLE IF NOT EXISTS books (
      id TEXT PRIMARY KEY,
      title TEXT NOT NULL,
      author TEXT NOT NULL,
      published_year INTEGER NOT NULL,
      genre TEXT NOT NULL,
      price REAL NOT NULL,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL
    )
  `);
}
```

## 근거 요약

- 근거: [문서] `backend-architecture/04-database/README.md`
- 근거: [문서] `backend-architecture/04-database/lab-report.md`
- 근거: [문서] `backend-architecture/04-database/express-impl/docs/README.md`
- 근거: [문서] `backend-architecture/04-database/express-impl/devlog/README.md`
