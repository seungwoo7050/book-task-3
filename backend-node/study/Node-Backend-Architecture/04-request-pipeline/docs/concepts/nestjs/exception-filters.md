# Exception Filters in NestJS

## Default Behavior

NestJS has a built-in exceptions layer. When an unhandled exception is thrown, it catches it and sends an appropriate user-friendly response:

```json
{ "statusCode": 500, "message": "Internal server error" }
```

For `HttpException` subclasses, NestJS uses the status code from the exception.

## Custom ExceptionFilter

To customize the error response format, implement `ExceptionFilter`:

```typescript
import {
  ExceptionFilter,
  Catch,
  ArgumentsHost,
  HttpException,
  HttpStatus,
} from "@nestjs/common";
import { Response } from "express";

@Catch()
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost): void {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();

    const status =
      exception instanceof HttpException
        ? exception.getStatus()
        : HttpStatus.INTERNAL_SERVER_ERROR;

    const message =
      exception instanceof HttpException
        ? exception.message
        : "Internal Server Error";

    response.status(status).json({
      success: false,
      error: {
        statusCode: status,
        message,
      },
    });
  }
}
```

## Applying Globally

```typescript
// main.ts
app.useGlobalFilters(new HttpExceptionFilter());
```

Or via the module system for dependency injection:

```typescript
@Module({
  providers: [{ provide: APP_FILTER, useClass: HttpExceptionFilter }],
})
export class AppModule {}
```

## Built-in HttpException Subclasses

| Exception               | Status |
|-------------------------|--------|
| `BadRequestException`   | 400    |
| `UnauthorizedException` | 401    |
| `ForbiddenException`    | 403    |
| `NotFoundException`     | 404    |
| `ConflictException`     | 409    |

## 근거 요약

- 근거: [문서] `backend-architecture/03-pipeline/README.md`
- 근거: [문서] `backend-architecture/03-pipeline/lab-report.md`
- 근거: [문서] `backend-architecture/03-pipeline/nestjs-impl/docs/README.md`
- 근거: [문서] `backend-architecture/03-pipeline/nestjs-impl/devlog/README.md`
