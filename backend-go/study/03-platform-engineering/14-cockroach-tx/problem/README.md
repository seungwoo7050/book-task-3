# Problem — CockroachDB Transactions

## Background

You are building an **inventory management service** for a game platform.
Players can purchase items, and the system must:

1. Deduct currency from the player's wallet.
2. Add the item to the player's inventory.
3. Record the transaction for auditing.

All three operations must succeed or fail together. The system must handle:
- **Concurrent purchases**: Two requests for the same item at the same time.
- **Duplicate requests**: A client retrying after a network timeout.
- **CockroachDB retries**: The database itself may ask you to retry.

## Requirements

### Part 1: Schema Design

Create the following tables:

```sql
CREATE TABLE players (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT NOT NULL,
    balance     BIGINT NOT NULL DEFAULT 0,
    version     INT NOT NULL DEFAULT 1,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE inventory (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id   UUID NOT NULL REFERENCES players(id),
    item_name   TEXT NOT NULL,
    quantity    INT NOT NULL DEFAULT 1,
    acquired_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (player_id, item_name)
);

CREATE TABLE idempotency_keys (
    key         TEXT PRIMARY KEY,
    player_id   UUID NOT NULL REFERENCES players(id),
    response    JSONB,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE audit_log (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id   UUID NOT NULL REFERENCES players(id),
    action      TEXT NOT NULL,
    detail      JSONB,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### Part 2: Optimistic Locking

Implement `DeductBalance(playerID, amount, expectedVersion)` that:
1. Updates balance only if `version = expectedVersion`.
2. Increments `version` on success.
3. Returns `ErrConflict` if the version has changed.

### Part 3: Idempotency

Implement `PurchaseItem(idempotencyKey, playerID, itemName, price)` that:
1. Checks `idempotency_keys` for a previous result.
2. If found, returns the cached response.
3. If not found, executes the purchase in a single transaction:
   a. Deduct balance (with optimistic locking).
   b. Insert/update inventory.
   c. Insert audit log entry.
   d. Insert idempotency key with response.

### Part 4: Transaction Retry

Implement a `RunInTx(ctx, db, fn)` helper that:
1. Begins a transaction.
2. Calls `fn(tx)`.
3. Commits.
4. If commit fails with SQLSTATE `40001`, retries from step 1.
5. Retries up to a configurable maximum (default 3).

### Part 5: HTTP API

Expose a simple HTTP endpoint:

```
POST /api/purchase
Content-Type: application/json
Idempotency-Key: <uuid>

{
  "player_id": "<uuid>",
  "item_name": "sword_of_fire",
  "price": 100
}
```

**Success (200)**:
```json
{
  "status": "ok",
  "new_balance": 900,
  "item": "sword_of_fire"
}
```

**Conflict (409)**:
```json
{
  "error": "balance version conflict, please retry"
}
```

**Duplicate (200)** — same response as the original.

## Evaluation Criteria

| Criteria | Weight |
|----------|--------|
| Correct optimistic locking implementation | 25% |
| Idempotency key handling | 25% |
| Transaction retry for 40001 errors | 20% |
| Clean separation (handler / service / repo) | 15% |
| Test coverage | 15% |
