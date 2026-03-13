# 16 GitOps Deploy 시리즈 맵

이 시리즈는 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 썼다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다.

## 이번 재작성 범위

- 문제 계약: [`README.md`](../../03-platform-engineering/16-gitops-deploy/README.md), [`problem/README.md`](../../03-platform-engineering/16-gitops-deploy/problem/README.md)
- 구현 표면:
- `solution/infra/Dockerfile`
- `solution/infra/charts/go-backend/templates/deployment.yaml`
- `solution/infra/k8s/argocd-app.yaml`
- `solution/infra/charts/go-backend/templates/configmap.yaml`
- `solution/infra/charts/go-backend/templates/hpa.yaml`
- `solution/infra/charts/go-backend/templates/secret.yaml`
- `solution/infra/charts/go-backend/templates/service.yaml`
- 검증 표면: `make -C problem helm-lint`, `make -C problem helm-template`
- 개념 축: `multi-stage Docker build는 빌드 환경과 런타임 환경을 분리한다.`, `Helm chart는 manifest를 값 중심으로 재사용하게 만든다.`, `ArgoCD Application은 “Git 상태를 클러스터에 동기화한다”는 선언적 모델이다.`

## 챕터 구성

1. [`01-evidence-ledger.md`](01-evidence-ledger.md)
   실제 코드, 테스트, CLI, git history에서 복원한 chronology ledger
2. [`_structure-outline.md`](_structure-outline.md)
   최종 blog를 어떤 순서와 코드 앵커로 전개할지 먼저 고정한 구조 설계
3. [`10-2026-03-13-reconstructed-development-log.md`](10-2026-03-13-reconstructed-development-log.md)
   구현 순서, 판단 전환점, 검증 신호를 한 편으로 다시 쓴 최종 blog

## 이번에 따라간 질문

Go API 한 개를 Docker image, Helm chart, ArgoCD Application으로 번역한다.
