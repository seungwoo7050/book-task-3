# Infra Implementation

- Scope: Dockerfile, Helm chart, ArgoCD manifest
- Build: `docker build -t ghcr.io/woopinbell/go-backend-api:latest -f 03-platform-engineering/16-gitops-deploy/infra/Dockerfile .`
- Test: `helm lint charts/go-backend` / `helm template go-backend charts/go-backend`
- Status: `verified`
- Effective build context: repository root with [.dockerignore](../../../.dockerignore)
- Known gaps: cluster apply smoke test은 선택 검증으로 남긴다.
