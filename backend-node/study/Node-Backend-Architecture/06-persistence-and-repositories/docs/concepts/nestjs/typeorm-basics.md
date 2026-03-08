# TypeORM Fundamentals

## What is TypeORM?

TypeORM is an ORM for TypeScript/JavaScript that supports Active Record and Data Mapper patterns. It works with PostgreSQL, MySQL, SQLite, and more.

## Entity Definition

An Entity maps a TypeScript class to a database table:

```typescript
import {
  Entity,
  PrimaryColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
} from "typeorm";

@Entity("books")
export class Book {
  @PrimaryColumn()
  id: string;

  @Column()
  title: string;

  @Column()
  author: string;

  @Column("integer")
  publishedYear: number;

  @Column()
  genre: string;

  @Column("real")
  price: number;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
```

## Repository API

TypeORM provides a built-in `Repository<Entity>` with CRUD methods:

| Method           | Description                          |
|-----------------|--------------------------------------|
| `find()`        | Fetch all records                    |
| `findOneBy()`   | Fetch one by conditions              |
| `save(entity)`  | Insert or update (upsert)            |
| `remove(entity)`| Delete the entity                    |
| `delete(id)`    | Delete by primary key                |

## DataSource Configuration

```typescript
const dataSource = new DataSource({
  type: "better-sqlite3",
  database: ":memory:",
  entities: [Book],
  synchronize: true, // Auto-create tables (dev only!)
});
```

## Column Type Mapping (SQLite)

| TypeORM Type   | SQLite Type |
|---------------|-------------|
| `string`      | TEXT        |
| `"integer"`   | INTEGER     |
| `"real"`      | REAL        |
| `"boolean"`   | INTEGER (0/1) |

## 근거 요약

- 근거: [문서] `backend-architecture/04-database/README.md`
- 근거: [문서] `backend-architecture/04-database/lab-report.md`
- 근거: [문서] `backend-architecture/04-database/nestjs-impl/docs/README.md`
- 근거: [문서] `backend-architecture/04-database/nestjs-impl/devlog/README.md`
