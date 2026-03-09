# G-ops-lab

- Status: `verified`
- Focus: health checks, metrics, Compose, CI expectations, and AWS-oriented docs
- FastAPI workspace: [fastapi/README.md](/Users/woopinbell/work/web-pong/labs/G-ops-lab/fastapi/README.md#L1)

## Scope

- live and ready checks
- structured JSON logging
- request-count metrics surface
- CI and AWS deployment guidance

## Validation

- `fastapi/` passes `make lint`, `make test`, and `make smoke`
- `fastapi/compose.yaml` passes live/ready probes
- CI now includes Compose health probing in addition to lint/test/smoke

## Intentional Simplifications

- metrics are intentionally minimal and Prometheus-compatible by shape, not a full observability stack
- AWS coverage is documentation-focused rather than infrastructure-as-code
