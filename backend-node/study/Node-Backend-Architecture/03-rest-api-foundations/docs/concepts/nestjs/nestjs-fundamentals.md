# NestJS Fundamentals

## What is NestJS?

NestJS is a **progressive, opinionated Node.js framework** for building efficient, reliable, and scalable server-side applications. It uses TypeScript by default and combines elements of **OOP (Object-Oriented Programming)**, **FP (Functional Programming)**, and **FRP (Functional Reactive Programming)**.

Under the hood, NestJS uses Express (by default) or Fastify as its HTTP platform. It adds a layer of **architecture and conventions** on top.

## Core Building Blocks

### 1. Modules (`@Module`)

Modules organize the application into cohesive blocks of functionality. Every NestJS app has at least one module — the **root module** (`AppModule`).

```typescript
import { Module } from "@nestjs/common";
import { BooksModule } from "./books/books.module";

@Module({
  imports: [BooksModule],
})
export class AppModule {}
```

A module's `@Module()` decorator accepts an object with:

| Property      | Purpose                                               |
| ------------- | ----------------------------------------------------- |
| `imports`     | Other modules whose exported providers this module needs |
| `controllers` | Controllers that belong to this module                 |
| `providers`   | Services (and other injectables) to be managed by the DI container |
| `exports`     | Providers that should be available to other modules    |

### 2. Controllers (`@Controller`)

Controllers handle incoming HTTP requests and return responses. They are analogous to Express routers + controllers combined.

```typescript
import { Controller, Get, Post, Body, Param } from "@nestjs/common";
import { BooksService } from "./books.service";
import { CreateBookDto } from "./dto/create-book.dto";

@Controller("books") // Handles routes under /books
export class BooksController {
  constructor(private readonly booksService: BooksService) {}

  @Get() // GET /books
  findAll() {
    return this.booksService.findAll();
  }

  @Get(":id") // GET /books/:id
  findOne(@Param("id") id: string) {
    return this.booksService.findOne(id);
  }

  @Post() // POST /books
  create(@Body() dto: CreateBookDto) {
    return this.booksService.create(dto);
  }
}
```

Key decorators:
- `@Controller("path")` — Declares a controller with a route prefix.
- `@Get()`, `@Post()`, `@Put()`, `@Delete()` — Map methods to HTTP verbs.
- `@Param("name")` — Extract route parameters.
- `@Body()` — Extract the parsed request body.
- `@HttpCode(204)` — Override the default status code.

### 3. Providers / Services (`@Injectable`)

Providers are classes that can be **injected** into other classes via the DI container. Services are the most common type of provider.

```typescript
import { Injectable } from "@nestjs/common";

@Injectable()
export class BooksService {
  private books = new Map<string, Book>();

  findAll(): Book[] {
    return Array.from(this.books.values());
  }
}
```

The `@Injectable()` decorator marks the class as manageable by the NestJS DI container. Registering it as a provider in a module makes it available for injection:

```typescript
@Module({
  controllers: [BooksController],
  providers: [BooksService], // Registered here
})
export class BooksModule {}
```

## Application Bootstrap

```typescript
import { NestFactory } from "@nestjs/core";
import { AppModule } from "./app.module";

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(3000);
}
bootstrap();
```

`NestFactory.create()` does what you did manually in Express:
1. Creates an Express app.
2. Scans all modules.
3. Instantiates all providers and controllers.
4. Wires dependencies via constructor injection.
5. Registers all routes from controller decorators.

## Exception Handling

NestJS provides built-in exception classes:

```typescript
import { NotFoundException } from "@nestjs/common";

@Get(":id")
findOne(@Param("id") id: string) {
  const book = this.booksService.findOne(id);
  if (!book) {
    throw new NotFoundException(`Book with ID "${id}" not found`);
  }
  return book;
}
```

This automatically returns a `404` response:
```json
{
  "statusCode": 404,
  "message": "Book with ID \"abc\" not found",
  "error": "Not Found"
}
```

No need for manual `res.status(404).json(...)`.

## Request Lifecycle

```
Client Request
    ↓
[Middleware]      →  (similar to Express middleware)
    ↓
[Guards]          →  Authentication/Authorization checks
    ↓
[Interceptors]   →  Pre-processing (logging, caching, transform)
    ↓
[Pipes]           →  Validation and transformation
    ↓
[Controller]      →  Route handler
    ↓
[Interceptors]   →  Post-processing (response mapping)
    ↓
[Exception Filter] → Error handling
    ↓
Client Response
```

For this assignment, you only need Controllers, Providers, and Modules. Guards, Interceptors, and Pipes will be covered in later chapters.

## 근거 요약

- 근거: [문서] `backend-architecture/01-rest-api/README.md`
- 근거: [문서] `backend-architecture/01-rest-api/lab-report.md`
- 근거: [문서] `backend-architecture/01-rest-api/nestjs-impl/docs/README.md`
- 근거: [문서] `backend-architecture/01-rest-api/nestjs-impl/devlog/README.md`
