# Problem — GitOps Deploy

## Background

You have built several Go services across the previous tasks. Now it's time
to package and deploy them to a Kubernetes cluster using a GitOps workflow.

The goal is to create a **production-ready deployment pipeline** where:
- Code changes trigger image builds.
- Configuration changes in Git automatically update the cluster.
- Rollbacks are as simple as `git revert`.

## Requirements

### Part 1: Dockerfile (Multi-Stage Build)

Create a Dockerfile for the API server (Task 01) that:

1. **Build stage**: Uses `golang:1.22-alpine` to compile the binary.
   - Sets `CGO_ENABLED=0` for a static binary.
   - Uses `go build -ldflags="-s -w"` to strip debug info.
2. **Runtime stage**: Uses `gcr.io/distroless/static-debian12`.
   - Copies only the compiled binary.
   - Sets a non-root user.
   - Exposes the service port.
   - Final image should be < 20MB.

### Part 2: Helm Chart

Create a Helm chart `go-backend` with:

1. **Chart.yaml**: Chart metadata (name, version, appVersion).
2. **values.yaml**: Default configuration values.
3. **Templates**:
   - `deployment.yaml` — Deployment with:
     - Configurable replicas
     - Resource requests/limits
     - Readiness and liveness probes
     - Environment variables from ConfigMap and Secrets
   - `service.yaml` — ClusterIP Service
   - `configmap.yaml` — Application configuration
   - `secret.yaml` — Database credentials (placeholder)
   - `hpa.yaml` — Horizontal Pod Autoscaler
   - `_helpers.tpl` — Template helper functions

### Part 3: ArgoCD Application

Create an ArgoCD Application manifest that:
1. Points to this Git repository's `charts/go-backend` directory.
2. Targets the `default` namespace.
3. Uses automated sync with self-heal and prune enabled.
4. Specifies the Helm value overrides for production.

### Part 4: .dockerignore

Create a `.dockerignore` that excludes:
- `.git/`
- `node_modules/`
- `*.md`
- `docs/`
- `devlog/`
- Test files

## Evaluation Criteria

| Criteria | Weight |
|----------|--------|
| Multi-stage Dockerfile correctness | 25% |
| Helm chart completeness and best practices | 30% |
| ArgoCD Application configuration | 20% |
| Security (non-root user, no secrets in image) | 15% |
| Documentation quality | 10% |
