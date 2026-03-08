# Problem: gRPC Microservices

## Objective

Build a **Product Catalog** microservice using gRPC with Protocol Buffers.
The service supports CRUD operations, server-side streaming for listing products,
and bidirectional streaming for real-time price updates.

## Service Definition

```protobuf
service ProductCatalog {
  rpc GetProduct(GetProductRequest) returns (Product);
  rpc CreateProduct(CreateProductRequest) returns (Product);
  rpc UpdateProduct(UpdateProductRequest) returns (Product);
  rpc DeleteProduct(DeleteProductRequest) returns (DeleteProductResponse);
  rpc ListProducts(ListProductsRequest) returns (stream Product);
  rpc PriceWatch(stream PriceWatchRequest) returns (stream PriceUpdate);
}
```

## Requirements

### Part 1: Proto Definition

1. Define the complete `.proto` file with all messages and the service.
2. Messages must include proper field types, numbering, and documentation.
3. Use `google.protobuf.Timestamp` for time fields.

### Part 2: Server Implementation

1. Implement all 6 RPC methods.
2. Use an in-memory store (similar to Task 01).
3. Implement a **logging interceptor** that logs every RPC call with:
   - Method name, duration, and status code.
4. Implement an **auth interceptor** that checks for a metadata key `authorization`.
5. Handle errors using proper gRPC status codes:
   - `NOT_FOUND`, `INVALID_ARGUMENT`, `ALREADY_EXISTS`, `UNAUTHENTICATED`.

### Part 3: Client Implementation

1. Implement a client that can call all 6 RPCs.
2. Use client-side round-robin load balancing.
3. Implement a **retry interceptor** with exponential backoff.

### Part 4: Streaming

1. `ListProducts` returns products one by one as a server stream.
2. `PriceWatch` is bidirectional: client sends product IDs to watch,
   server sends back price updates when prices change.

## Evaluation Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Proto design | 20% | Well-structured proto file with proper types |
| Server correctness | 25% | All RPCs work correctly |
| Interceptors | 20% | Logging and auth interceptors work properly |
| Streaming | 20% | Both streaming patterns work correctly |
| Client + tests | 15% | Client works; integration tests pass |
