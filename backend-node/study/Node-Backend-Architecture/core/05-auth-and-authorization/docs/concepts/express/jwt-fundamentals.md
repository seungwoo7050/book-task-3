# JSON Web Tokens (JWT)

## What is JWT?

JSON Web Token is an open standard (RFC 7519) for securely transmitting information between parties as a JSON object. It is **self-contained** — the token itself contains all the information needed to verify the user, without querying a database.

## Structure

A JWT has three parts separated by dots: `header.payload.signature`

```
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjMiLCJ1c2VybmFtZSI6ImpvaG4ifQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

### Header
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

### Payload (Claims)
```json
{
  "sub": "user-id-123",
  "username": "john",
  "role": "ADMIN",
  "iat": 1700000000,
  "exp": 1700003600
}
```

Standard claims:
- `sub` (subject) — Who the token identifies.
- `iat` (issued at) — When the token was created.
- `exp` (expiration) — When the token expires.

### Signature
```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

The signature ensures the token has not been tampered with.

## Using `jsonwebtoken` in Node.js

### Signing (Creating a Token)

```typescript
import jwt from "jsonwebtoken";

const SECRET = "my-secret-key";

const token = jwt.sign(
  { sub: user.id, username: user.username, role: user.role },
  SECRET,
  { expiresIn: "1h" }
);
```

### Verifying (Validating a Token)

```typescript
try {
  const decoded = jwt.verify(token, SECRET);
  // decoded = { sub: "...", username: "...", role: "...", iat: ..., exp: ... }
} catch (err) {
  // Token is invalid or expired
}
```

## Bearer Token Pattern

The standard way to send a JWT in an HTTP request is via the `Authorization` header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...
```

The middleware extracts the token:

```typescript
const authHeader = req.headers.authorization;
if (!authHeader || !authHeader.startsWith("Bearer ")) {
  return res.status(401).json({ error: "No token provided" });
}
const token = authHeader.split(" ")[1];
```

## Security Considerations

1. **Never store secrets in code** for production. Use environment variables.
2. **Always set expiration** (`expiresIn`) to limit token lifetime.
3. **Hash passwords** before storing — never store plaintext passwords.
4. **Use HTTPS** — JWTs are not encrypted, only signed. Anyone intercepting the token can read the payload.

## 근거 요약

- 근거: [문서] `backend-architecture/02-auth-guards/README.md`
- 근거: [문서] `backend-architecture/02-auth-guards/lab-report.md`
- 근거: [문서] `backend-architecture/02-auth-guards/express-impl/docs/README.md`
- 근거: [문서] `backend-architecture/02-auth-guards/express-impl/devlog/README.md`
