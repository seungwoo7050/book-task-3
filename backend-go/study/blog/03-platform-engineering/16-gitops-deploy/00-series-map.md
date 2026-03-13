# 16 GitOps Deploy Series Map

`03-platform-engineering/16-gitops-deploy`는 Docker multi-stage build, Helm chart, ArgoCD manifest를 통해 코드 자산을 배포 자산으로 번역하는 인프라 과제다.

## 이 시리즈가 복원하는 것

- 시작점: Go 서비스용 multi-stage Dockerfile을 작성해야 한다.
- 구현 축: Dockerfile, Helm chart, ArgoCD manifest를 `solution/infra`에 구성했다.
- 검증 축: 2026-03-07 기준 `make test-infra`가 통과했다.
- 글 수: 3편

## 읽는 순서

- [10-docker-build-surface.md](10-docker-build-surface.md)
- [20-helm-chart-and-runtime-shape.md](20-helm-chart-and-runtime-shape.md)
- [30-argocd-and-infra-proof.md](30-argocd-and-infra-proof.md)

## 근거 기준

- 소스코드, README, docs, 테스트, CLI만 입력 근거로 사용했다.
- 기존 blog 초안과 `_legacy` 본문은 입력 근거로 사용하지 않았다.
