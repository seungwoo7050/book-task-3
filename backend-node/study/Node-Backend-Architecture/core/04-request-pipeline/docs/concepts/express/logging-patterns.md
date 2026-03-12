# Request Logging Patterns

## Basic Logger Middleware

```typescript
function requestLogger(req: Request, res: Response, next: NextFunction): void {
  const start = Date.now();

  // Listen for the response to finish
  res.on("finish", () => {
    const duration = Date.now() - start;
    console.log(
      `[${new Date().toISOString()}] ${req.method} ${req.originalUrl} — ${res.statusCode} in ${duration}ms`
    );
  });

  next();
}
```

The key is using `res.on("finish", ...)` which fires after the response is fully sent to the client. At that point, `res.statusCode` is the final status code.

## Structured Logging

For production, structured JSON logging is preferred:

```typescript
res.on("finish", () => {
  const log = {
    timestamp: new Date().toISOString(),
    method: req.method,
    url: req.originalUrl,
    statusCode: res.statusCode,
    durationMs: Date.now() - start,
    contentLength: res.get("Content-Length"),
  };
  console.log(JSON.stringify(log));
});
```

## Registration Order

The logger must be registered **before** all routes:

```typescript
const app = express();
app.use(requestLogger);  // First — captures all requests
app.use(express.json());
app.use("/books", bookRouter);
app.use(errorHandler);   // Last — catches all errors
```

## 근거 요약

- 근거: [문서] `backend-architecture/03-pipeline/README.md`
- 근거: [문서] `backend-architecture/03-pipeline/lab-report.md`
- 근거: [문서] `backend-architecture/03-pipeline/express-impl/docs/README.md`
- 근거: [문서] `backend-architecture/03-pipeline/express-impl/devlog/README.md`
