# Solution

## 답안 요약

- 구현 위치: `solution/infra`
- 핵심 범위: Dockerfile, Helm chart, ArgoCD manifest
- 이 답안은 `verified` 상태 기준으로 공개 표면을 정리했다.

## 구현 진입점

- `docker build -t ghcr.io/woopinbell/go-backend-api:latest -f study/03-platform-engineering/16-gitops-deploy/solution/infra/Dockerfile .`
- `cd study/03-platform-engineering/16-gitops-deploy/solution/infra && helm lint charts/go-backend`
- `cd study/03-platform-engineering/16-gitops-deploy/solution/infra && helm template go-backend charts/go-backend`

## 현재 한계

- cluster apply smoke test은 선택 검증으로 남긴다.
