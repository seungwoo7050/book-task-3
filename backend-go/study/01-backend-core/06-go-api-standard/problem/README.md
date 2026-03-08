# Problem: Go API Standard

## Objective

Design and implement a **RESTful JSON API** for a simple **Movie** resource
using only Go's standard library.

## Requirements

### Functional Requirements

1. **Healthcheck endpoint**: `GET /v1/healthcheck` returns server status and version.
2. **CRUD for Movies**:
   - `POST /v1/movies` — Create a new movie.
   - `GET /v1/movies/:id` — Read a single movie by ID.
   - `GET /v1/movies` — List movies with pagination and filtering.
   - `PATCH /v1/movies/:id` — Partial update of a movie.
   - `DELETE /v1/movies/:id` — Delete a movie.
3. **JSON envelope**: All responses must follow a consistent envelope format:
   ```json
   {
     "data": { "movie": { ... } },
     "meta": { "current_page": 1, "page_size": 20 }
   }
   ```
   Error responses:
   ```json
   {
     "error": { "message": "record not found" }
   }
   ```
4. **Input validation**: Validate all incoming data (e.g., year > 1888, runtime > 0).
5. **Pagination**: Support `page` and `page_size` query parameters.

### Non-Functional Requirements

1. **No external dependencies** for routing or HTTP handling.
2. **Graceful shutdown**: On SIGINT/SIGTERM, stop accepting new connections, wait for
   in-flight requests (up to 30s), then exit cleanly.
3. **Structured logging** using `log/slog` or the common logger module.
4. **Configuration via environment variables**: `PORT`, `ENV` (development/staging/production).
5. **Middleware stack**: Implement at least:
   - Request logging (method, URI, status, duration)
   - Panic recovery
   - CORS headers

### Constraints

- Go 1.22+ (use the new `ServeMux` pattern matching: `GET /v1/movies/{id}`).
- No third-party router packages.
- No ORM — use `database/sql` if a DB is involved, or an in-memory store for simplicity.

## Data Model

```go
type Movie struct {
    ID        int64     `json:"id"`
    CreatedAt time.Time `json:"created_at"`
    Title     string    `json:"title"`
    Year      int32     `json:"year"`
    Runtime   int32     `json:"runtime"` // in minutes
    Genres    []string  `json:"genres"`
    Version   int32     `json:"version"`
}
```

## Evaluation Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Correctness | 30% | All endpoints work as specified |
| Code structure | 25% | Clean separation of concerns (handler/model/middleware) |
| Error handling | 20% | Proper HTTP status codes, consistent error envelope |
| Graceful shutdown | 15% | Server handles SIGINT/SIGTERM correctly |
| Tests | 10% | Table-driven unit tests for handlers and validators |

## Starter Code

See `code/` for a minimal project skeleton with `main.go` and directory layout.

## Test Script

```bash
make test        # Run unit tests
make run         # Start the server
make healthcheck # curl the healthcheck endpoint
```
