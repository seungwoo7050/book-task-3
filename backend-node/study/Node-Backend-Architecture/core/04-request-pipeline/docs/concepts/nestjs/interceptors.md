# Interceptors in NestJS

## What is an Interceptor?

An Interceptor is a class annotated with `@Injectable()` that implements `NestInterceptor`. They can:

1. **Bind extra logic** before/after method execution
2. **Transform** the result returned from a function
3. **Transform** the exception thrown from a function
4. **Extend** basic function behavior (e.g., caching, logging)

## The `intercept()` Method

```typescript
intercept(context: ExecutionContext, next: CallHandler): Observable<any>
```

- `context`: The current execution context (access to request, etc.)
- `next.handle()`: Returns an `Observable` wrapping the route handler's response
- Code before `next.handle()` runs BEFORE the handler
- Operators on the Observable (e.g., `tap`, `map`) run AFTER the handler

## Logging Interceptor

```typescript
@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const req = context.switchToHttp().getRequest();
    const { method, url } = req;
    const start = Date.now();

    return next.handle().pipe(
      tap(() => {
        const duration = Date.now() - start;
        console.log(`${method} ${url} — ${duration}ms`);
      }),
    );
  }
}
```

## Transform Interceptor (Response Wrapping)

```typescript
@Injectable()
export class TransformInterceptor<T> implements NestInterceptor<T, { success: true; data: T }> {
  intercept(context: ExecutionContext, next: CallHandler<T>): Observable<{ success: true; data: T }> {
    return next.handle().pipe(
      map((data) => ({ success: true as const, data })),
    );
  }
}
```

## Registration

```typescript
// Global
app.useGlobalInterceptors(new LoggingInterceptor(), new TransformInterceptor());

// Controller level
@UseInterceptors(LoggingInterceptor)
@Controller("books")
export class BooksController {}
```

## Execution Order

```
Request → Middleware → Guards → Interceptors (pre) → Pipes → Handler → Interceptors (post) → Response
```

## 근거 요약

- 근거: [문서] `backend-architecture/03-pipeline/README.md`
- 근거: [문서] `backend-architecture/03-pipeline/lab-report.md`
- 근거: [문서] `backend-architecture/03-pipeline/nestjs-impl/docs/README.md`
- 근거: [문서] `backend-architecture/03-pipeline/nestjs-impl/devlog/README.md`
