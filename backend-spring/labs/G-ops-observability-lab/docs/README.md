# G-ops-observability-lab Notes

## Implemented now

- JSON logging with trace ID header propagation
- health endpoints and Prometheus scrape target
- Compose stack including Prometheus
- GitHub Actions validation workflow

## Important simplifications

- metrics are exposed, but no alert rules are authored yet
- logs are structured, but not shipped to an external platform
- AWS deployment is documented direction, not validated infrastructure code

## Next improvements

- add alert examples and dashboard suggestions
- add AWS deployment assets or IaC
- extend smoke tests to check `/actuator/prometheus`
