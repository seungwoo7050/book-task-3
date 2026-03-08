# Passport JWT Strategy in NestJS

## Overview

NestJS integrates with Passport.js via `@nestjs/passport`. Instead of manually verifying JWTs in middleware, you create a **Strategy** class that tells Passport how to validate tokens.

## Setup

### 1. Install Packages

```bash
pnpm add @nestjs/passport @nestjs/jwt passport passport-jwt
pnpm add -D @types/passport-jwt
```

### 2. Create JWT Strategy

```typescript
import { Injectable } from "@nestjs/common";
import { PassportStrategy } from "@nestjs/passport";
import { ExtractJwt, Strategy } from "passport-jwt";

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor() {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: "super-secret",
    });
  }

  // Called after JWT is verified — return value becomes req.user
  validate(payload: any) {
    return { sub: payload.sub, username: payload.username, role: payload.role };
  }
}
```

### 3. Create JwtAuthGuard

```typescript
import { Injectable } from "@nestjs/common";
import { AuthGuard } from "@nestjs/passport";

@Injectable()
export class JwtAuthGuard extends AuthGuard("jwt") {}
```

### 4. Configure AuthModule

```typescript
import { Module } from "@nestjs/common";
import { JwtModule } from "@nestjs/jwt";
import { PassportModule } from "@nestjs/passport";
import { JwtStrategy } from "./strategies/jwt.strategy";

@Module({
  imports: [
    PassportModule,
    JwtModule.register({
      secret: "super-secret",
      signOptions: { expiresIn: "1h" },
    }),
  ],
  providers: [AuthService, JwtStrategy],
  controllers: [AuthController],
})
export class AuthModule {}
```

## How It Works

1. Request with `Authorization: Bearer <token>` arrives.
2. `@UseGuards(JwtAuthGuard)` triggers the JWT Passport strategy.
3. Passport extracts the token from the header.
4. Passport verifies the signature and expiration.
5. `validate()` is called with the decoded payload.
6. The return value of `validate()` is attached to `req.user`.
7. The guard returns `true` (allow) or throws `UnauthorizedException`.

## Comparison with Express

| Express                           | NestJS                                  |
| --------------------------------- | --------------------------------------- |
| Manual `jwt.verify()` in middleware | Passport strategy + `AuthGuard`         |
| `req.user = decoded`              | `validate()` return → `req.user`       |
| `if (!req.user) res.status(401)` | Guard throws `UnauthorizedException`   |

## 근거 요약

- 근거: [문서] `backend-architecture/02-auth-guards/README.md`
- 근거: [문서] `backend-architecture/02-auth-guards/lab-report.md`
- 근거: [문서] `backend-architecture/02-auth-guards/nestjs-impl/docs/README.md`
- 근거: [문서] `backend-architecture/02-auth-guards/nestjs-impl/devlog/README.md`
