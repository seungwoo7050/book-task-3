# NestJS Guards

## What is a Guard?

A Guard is a class decorated with `@Injectable()` that implements the `CanActivate` interface. Guards determine whether a given request will be handled by the route handler, based on certain conditions (e.g., authentication, roles, permissions).

```typescript
import { Injectable, CanActivate, ExecutionContext } from "@nestjs/common";

@Injectable()
export class AuthGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    return !!request.user; // Allow only if user is attached
  }
}
```

## Guard vs Middleware

| Aspect         | Middleware                     | Guard                           |
| -------------- | ------------------------------ | ------------------------------- |
| Awareness      | No knowledge of what runs next | Knows the exact route handler   |
| Context        | Only `req`, `res`, `next`      | Full `ExecutionContext`          |
| Return Value   | Void (calls `next()`)          | Boolean (allow/deny)            |
| Use Case       | Logging, CORS, body parsing    | Auth, authz, rate limiting      |

## ExecutionContext

The `ExecutionContext` extends `ArgumentsHost` and provides additional information about the current execution context:

```typescript
canActivate(context: ExecutionContext): boolean {
  const request = context.switchToHttp().getRequest();
  const handler = context.getHandler();   // The route handler method
  const controller = context.getClass();   // The controller class
  return true;
}
```

## Using Reflector for Metadata

The `Reflector` class reads metadata set by custom decorators. This is how `@Roles("ADMIN")` communicates with `RolesGuard`:

### 1. Define the Decorator

```typescript
import { SetMetadata } from "@nestjs/common";
export const Roles = (...roles: string[]) => SetMetadata("roles", roles);
```

### 2. Apply to a Route

```typescript
@Post()
@Roles("ADMIN")
create(@Body() dto: CreateBookDto) { ... }
```

### 3. Read in the Guard

```typescript
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.getAllAndOverride<string[]>("roles", [
      context.getHandler(),
      context.getClass(),
    ]);
    if (!requiredRoles) return true; // No roles required
    const { user } = context.switchToHttp().getRequest();
    return requiredRoles.includes(user.role);
  }
}
```

## Applying Guards

```typescript
// On a single route
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles("ADMIN")
@Post()
create() { ... }

// On a controller (all routes)
@UseGuards(JwtAuthGuard)
@Controller("books")
export class BooksController { ... }

// Globally
app.useGlobalGuards(new JwtAuthGuard());
```

## 근거 요약

- 근거: [문서] `backend-architecture/02-auth-guards/README.md`
- 근거: [문서] `backend-architecture/02-auth-guards/lab-report.md`
- 근거: [문서] `backend-architecture/02-auth-guards/nestjs-impl/docs/README.md`
- 근거: [문서] `backend-architecture/02-auth-guards/nestjs-impl/devlog/README.md`
