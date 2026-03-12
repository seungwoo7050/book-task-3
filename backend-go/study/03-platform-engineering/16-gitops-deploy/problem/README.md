# 문제 정의

Go 서비스 코드를 Kubernetes GitOps 배포 자산으로 패키징한다.

## 성공 기준

- multi-stage Dockerfile을 작성한다.
- Helm chart에 Deployment, Service, ConfigMap, Secret, HPA 등을 포함한다.
- ArgoCD Application manifest를 제공한다.
- `.dockerignore`와 보안 기본값을 맞춘다.

## 제공 자료와 출처

- legacy `03-platform-engineering/08-gitops-deploy` 문제를 한국어 canonical 형태로 다시 정리한 문서다.
- 원문 요구사항은 provenance로만 유지한다.
- 공개 구현은 [`solution/README.md`](../solution/README.md)와 `solution/infra`에 둔다.

## 검증 기준

- `make -C problem docker-build`
- `make -C problem helm-lint`
- `make -C problem helm-template`

## 제외 범위

- 실제 Kubernetes cluster 적용
- 운영 ArgoCD smoke test
