# Pipes & ValidationPipe in NestJS

## What is a Pipe?

A Pipe is a class annotated with `@Injectable()` that implements `PipeTransform`. Pipes have two typical use cases:

1. **Transformation** — transform input data to a desired form (e.g., string to integer)
2. **Validation** — evaluate input data and throw if invalid

## Built-in ValidationPipe

NestJS provides a `ValidationPipe` that uses `class-validator` and `class-transformer`:

```typescript
// main.ts
app.useGlobalPipes(
  new ValidationPipe({
    whitelist: true,              // Strip properties not in DTO
    forbidNonWhitelisted: true,   // Throw if unknown properties sent
    transform: true,              // Auto-transform payloads to DTO instances
  }),
);
```

## class-validator Decorators

```typescript
import { IsString, IsNumber, IsInt, IsPositive, Min, Max, MinLength } from "class-validator";

export class CreateBookDto {
  @IsString()
  @MinLength(1)
  title: string;

  @IsString()
  @MinLength(1)
  author: string;

  @IsInt()
  @Min(1000)
  @Max(2100)
  publishedYear: number;

  @IsString()
  @MinLength(1)
  genre: string;

  @IsNumber()
  @IsPositive()
  price: number;
}
```

## PartialType for Updates

```typescript
import { PartialType } from "@nestjs/common";

export class UpdateBookDto extends PartialType(CreateBookDto) {}
```

`PartialType` makes all properties optional while preserving the validation decorators. It requires `@nestjs/mapped-types`.

## Execution Order

Pipes execute **after** Guards but **before** the route handler:

```
Client → Middleware → Guards → Interceptors (pre) → Pipes → Handler → Interceptors (post)
```

## 근거 요약

- 근거: [문서] `backend-architecture/03-pipeline/README.md`
- 근거: [문서] `backend-architecture/03-pipeline/lab-report.md`
- 근거: [문서] `backend-architecture/03-pipeline/nestjs-impl/docs/README.md`
- 근거: [문서] `backend-architecture/03-pipeline/nestjs-impl/devlog/README.md`
