# Concurrency And Cache

The proxylab migration is organized around three milestones:

1. sequential forwarding
2. detached per-connection threading
3. caching

The finished `study/` implementation reaches all three.

## Threading Model

Each accepted client connection is handed to a detached thread.

That keeps the main accept loop simple:

- accept
- heap-allocate the connected fd
- create a detached thread
- continue accepting immediately

The concurrency test in this project intentionally uses two slow origin requests to make sure the
proxy is not accidentally still sequential.

## Cache Design

The cache is process-wide and stores complete HTTP response bytes.

Each entry stores:

- the request URI as the key
- a heap copy of the response bytes
- response size
- previous and next pointers for LRU ordering

The policy is:

- cache only objects up to `MAX_OBJECT_SIZE`
- evict from the tail while total size exceeds `MAX_CACHE_SIZE`
- promote on hit

## Locking Discipline

The cache uses one mutex.

That is intentionally conservative.
The pedagogical target here is not lock-free or fine-grained caching.
It is:

- understanding shared state
- keeping LRU mutation correct
- avoiding data races between concurrent handlers

On cache hit, the proxy copies the object out while holding the lock and writes the copy after
unlocking.
That avoids holding the cache lock across client I/O.
