# NestJS Integration Architecture

## Module Composition

A production NestJS application is composed of feature modules, each encapsulating a bounded context. The capstone integrates five key modules:

```
AppModule
├── TypeOrmModule.forRoot()         [Ch04: Database]
├── EventEmitterModule.forRoot()    [Ch05: Events]
├── AuthModule                      [Ch02: JWT + Guards]
│   ├── JwtStrategy (Passport)
│   ├── AuthService (bcrypt + JWT)
│   └── AuthController
├── BooksModule                     [Ch01: REST + Ch04: TypeORM]
│   ├── BooksController
│   ├── BooksService → EventEmitter2
│   └── TypeOrmModule.forFeature([Book])
└── EventsModule                    [Ch05: Listeners]
    └── BookEventListener (@OnEvent)
```

## Request Lifecycle

Every HTTP request flows through a well-defined pipeline:

```
HTTP Request
  → Global Pipes (ValidationPipe)           [Ch03]
    → Guards (JwtAuthGuard → RolesGuard)    [Ch02]
      → Interceptors (Logging, Transform)   [Ch03]
        → Controller → Service              [Ch01]
          → Repository (TypeORM)            [Ch04]
          → EventEmitter2.emit()            [Ch05]
        ← Interceptors (response wrapping)
      ← Guards (pass-through on success)
    ← Pipes (pass-through on success)
  ← Exception Filter (error formatting)    [Ch03]
HTTP Response
```

## Authentication Flow

```
POST /auth/register
  → ValidationPipe → AuthService.register()
    → bcrypt.hash() → userRepository.save()
    → emit("user.registered")
  ← { id, username, role }

POST /auth/login
  → ValidationPipe → AuthService.login()
    → userRepository.findOneBy(username)
    → bcrypt.compare()
    → jwtService.sign({ sub: user.id, username, role })
  ← { accessToken: "eyJ..." }

GET /books (public)
  → No guard required
  → BooksController.findAll()

POST /books (admin only)
  → JwtAuthGuard (validate token)
    → RolesGuard (check ADMIN role)
      → BooksController.create()
        → BooksService.create() → emit("book.created")
```

## Guard Composition

Guards execute in order: `JwtAuthGuard` first (authenticates), then `RolesGuard` (authorizes):

```typescript
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles(Role.ADMIN)
@Post()
create(@Body() dto: CreateBookDto) { ... }
```

### Public vs Protected Routes

- **Public**: `GET /books`, `GET /books/:id`, `POST /auth/register`, `POST /auth/login`
- **Protected (any authenticated)**: None beyond admin routes in this app
- **Admin only**: `POST /books`, `PUT /books/:id`, `DELETE /books/:id`

## Event Architecture

Events decouple CRUD from side effects:

```
BooksService.create()
  → bookRepository.save()
  → eventEmitter.emit("book.created", new BookCreatedEvent(...))
    ├── BookEventListener.handleBookCreated()  → console.log
    └── (future: NotificationListener, CacheListener, etc.)
```

This enables adding new side effects without modifying `BooksService`.

## Error Handling Strategy

```
Application Error
  → HttpException hierarchy
    → HttpExceptionFilter.catch()
      → Structured JSON: { success: false, error: { status, message, details? } }
```

1. **Validation errors** (400): Thrown by `ValidationPipe`, caught by filter
2. **Auth errors** (401): Thrown by `JwtAuthGuard` (UnauthorizedException)
3. **Role errors** (403): Thrown by `RolesGuard` (ForbiddenException)
4. **Not found** (404): Thrown by service (NotFoundException)
5. **Unknown errors** (500): Caught by filter as fallback
