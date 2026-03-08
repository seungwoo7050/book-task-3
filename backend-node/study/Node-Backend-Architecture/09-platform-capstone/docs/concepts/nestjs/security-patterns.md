# Security Patterns in NestJS

## JWT Authentication

### Token Structure

A JWT consists of three parts: Header, Payload, Signature.

```
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyLWlkIiwidXNlcm5hbWUiOiJhZG1pbiIsInJvbGUiOiJBRE1JTiJ9.signature
```

Payload for this application:

```json
{
  "sub": "user-uuid",
  "username": "admin",
  "role": "ADMIN",
  "iat": 1700000000,
  "exp": 1700003600
}
```

### Passport JWT Strategy

`@nestjs/passport` provides `PassportStrategy` to integrate Passport.js strategies:

```typescript
@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor() {
    super({
      jwtFromRequest: ExtractJwt.fromAuthBearerToken(),
      secretOrKey: "secret",
    });
  }

  validate(payload: JwtPayload): RequestUser {
    return { id: payload.sub, username: payload.username, role: payload.role };
  }
}
```

The `validate()` return value is attached to `req.user`.

### JwtAuthGuard

```typescript
@Injectable()
export class JwtAuthGuard extends AuthGuard("jwt") {}
```

This guard:
1. Extracts JWT from `Authorization: Bearer <token>`
2. Verifies signature and expiration
3. Calls `JwtStrategy.validate()`
4. Attaches result to request

## Role-Based Authorization

### Role Enum

```typescript
export enum Role {
  USER = "USER",
  ADMIN = "ADMIN",
}
```

### @Roles Decorator

Custom decorator that attaches metadata:

```typescript
export const Roles = (...roles: Role[]) => SetMetadata("roles", roles);
```

### RolesGuard

Reads metadata and checks against `req.user.role`:

```typescript
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const roles = this.reflector.getAllAndOverride<Role[]>("roles", [
      context.getHandler(),
      context.getClass(),
    ]);
    if (!roles) return true; // No @Roles → public
    const { user } = context.switchToHttp().getRequest();
    return roles.includes(user.role);
  }
}
```

## Password Hashing

Use `bcryptjs` for secure password hashing:

```typescript
// Registration
const hash = await bcrypt.hash(password, 10);

// Login verification
const isValid = await bcrypt.compare(inputPassword, storedHash);
```

**Never store plain-text passwords.** bcrypt includes salt in the hash output, so no separate salt storage is needed.

## Security Checklist

- [x] Passwords hashed with bcrypt (cost factor 10)
- [x] JWT with expiration (1 hour)
- [x] Secret key configurable via environment variable
- [x] Guards applied per-route, not globally (allows public endpoints)
- [x] Role check happens after authentication (guard ordering)
- [x] Validation prevents injection via class-validator whitelist
