# F-cache-concurrency-lab Notes

## Implemented now

- inventory lookup endpoint
- reservation endpoint with idempotency-key handling
- cacheable inventory status path

## Important simplifications

- test runs use an in-memory `CacheManager` instead of a real Redis cache
- reservation logic is synchronized in-process rather than distributed
- Redisson locking is still a next step, not implemented behavior

## Next improvements

- switch selected flows to Redis-backed cache assertions
- add distributed lock implementation and conflict tests
- separate idempotency persistence from inventory persistence
