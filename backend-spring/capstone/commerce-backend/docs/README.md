# commerce-backend Notes

## Implemented now

- login surface and `me` endpoint
- admin product creation and public product listing
- cart item creation and order placement
- stock decrement through checkout
- Compose stack with PostgreSQL, Redis, Mailpit, and Redpanda

## Important simplifications

- auth is contract-level only and not yet a full Spring Security commerce stack
- payment is omitted entirely
- notifications and event consumers are not fully wired into the capstone runtime

## Why the modular monolith choice matters

- the repository is for learning backend composition, not service choreography
- the capstone should be understandable from one codebase without infrastructure sprawl
- the labs can be recomposed without importing their code directly
