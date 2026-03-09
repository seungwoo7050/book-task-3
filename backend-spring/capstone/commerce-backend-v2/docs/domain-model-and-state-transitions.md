# Domain Model And State Transitions

## Main tables

- `users`, `user_roles`, `refresh_tokens`, `oauth_accounts`, `audit_events`
- `categories`, `products`
- `orders`, `order_items`, `inventory_reservations`
- `payments`
- `outbox_events`, `notifications`

## Order lifecycle

- `PENDING_PAYMENT`
  - created by checkout after stock reservation succeeds
  - valid next states: `PAID`, `CANCELLED`
- `PAID`
  - set by mock payment confirmation
  - valid next state: `FULFILLED`
- `CANCELLED`
  - terminal
  - releases inventory reservations if cancellation happens before payment
- `FULFILLED`
  - terminal

## Inventory lifecycle

- product stock is decremented during checkout, not payment
- each reserved line creates an `inventory_reservations` row with `RESERVED`
- payment confirmation marks reservations `CONFIRMED`
- cancellation before payment releases stock and marks reservations `RELEASED`
- `products.version` is used for optimistic locking so concurrent checkout conflicts fail fast

## Payment lifecycle

- only one payment record exists per order
- `Idempotency-Key` is unique
- same idempotency key replays the existing payment response
- different idempotency keys against an already-paid order are rejected

## Event lifecycle

- payment confirmation inserts an `outbox_events` row
- scheduled publisher sends pending rows to Kafka/Redpanda
- consumer stores a deduplicated notification using `notifications.dedup_key`

