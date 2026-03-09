# F-realtime-lab

- Status: `verified`
- Focus: WebSocket auth, presence heartbeat, and notification fan-out
- FastAPI workspace: [fastapi/README.md](/Users/woopinbell/work/web-pong/labs/F-realtime-lab/fastapi/README.md#L1)

## Scope

- websocket connection auth
- presence heartbeat with TTL expiry
- fan-out to multiple active sockets
- reconnect-friendly HTTP support surfaces

## Validation

- `fastapi/` passes `make lint`, `make test`, and `make smoke`
- `fastapi/compose.yaml` passes live/ready probes

## Intentional Simplifications

- in-memory runtime state is used in tests and local app logic
- Redis is documented as the scaling boundary, not fully wired into fan-out logic yet
