# 16-gitops-deploy 문제지

## 왜 중요한가

Go 서비스 코드를 Kubernetes GitOps 배포 자산으로 패키징한다.

## 목표

시작 위치의 구현을 완성해 multi-stage Dockerfile을 작성한다, Helm chart에 Deployment, Service, ConfigMap, Secret, HPA 등을 포함한다, ArgoCD Application manifest를 제공한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/.dockerignore`
- `../study/03-platform-engineering/16-gitops-deploy/solution/infra/charts/go-backend/Chart.yaml`
- `../study/03-platform-engineering/16-gitops-deploy/solution/infra/charts/go-backend/templates/configmap.yaml`
- `../study/03-platform-engineering/16-gitops-deploy/problem/Makefile`

## starter code / 입력 계약

- `../study/.dockerignore`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- multi-stage Dockerfile을 작성한다.
- Helm chart에 Deployment, Service, ConfigMap, Secret, HPA 등을 포함한다.
- ArgoCD Application manifest를 제공한다.
- dockerignore와 보안 기본값을 맞춘다.

## 제외 범위

- 실제 Kubernetes cluster 적용
- 운영 ArgoCD smoke test
- `../study/.dockerignore` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.

## 성공 체크리스트

- `../study/.dockerignore` 등 fixture/trace 기준으로 결과를 대조했다.
- `make -C /Users/woopinbell/work/book-task-3/backend-go/study/03-platform-engineering/16-gitops-deploy/problem helm-lint`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/backend-go/study/03-platform-engineering/16-gitops-deploy/problem helm-lint
```

- Helm 검증은 현재 셸에 `helm` CLI가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`16-gitops-deploy_answer.md`](16-gitops-deploy_answer.md)에서 확인한다.
