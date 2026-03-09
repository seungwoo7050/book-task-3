# 문제 정의 — 코드를 넘어 인프라까지

## 왜 이 프로젝트인가

지금까지 Go 서비스를 여러 개 만들었다. 하지만 `go run ./cmd/server`로 실행하는 것은 프로덕션이 아니다. 실제 서비스는 컨테이너에 패키징되고, 오케스트레이터(Kubernetes)에 배포되고, 설정 변경이 추적 가능해야 한다.

이 프로젝트의 핵심 물음: **"Git이 진실의 원천(Source of Truth)이 되면, 배포는 어떻게 바뀌는가?"**

## GitOps란

전통적 배포: 개발자가 서버에 SSH → 바이너리 교체 → 서비스 재시작.
CI/CD 배포: 파이프라인이 빌드 → 테스트 → 배포를 자동화.
GitOps 배포: **Git 리포지토리의 상태가 곧 클러스터의 원하는 상태**. ArgoCD 같은 에이전트가 Git과 클러스터를 동기화한다.

차이: CI/CD는 "이 코드를 배포하라"(push), GitOps는 "클러스터가 이 상태여야 한다"(pull). 롤백은 `git revert`로 끝난다.

## 세 가지 산출물

1. **Dockerfile**: Go 서비스를 20MB 미만의 컨테이너 이미지로 패키징
2. **Helm Chart**: Kubernetes 리소스(Deployment, Service, HPA 등)를 템플릿화
3. **ArgoCD Application**: Git → 클러스터 자동 동기화 설정

이 프로젝트는 Go 코드를 작성하지 않는다. 대신 Go 서비스가 프로덕션으로 가는 길을 닦는다.

## 대상 애플리케이션

프로젝트 06 (go-api-standard)의 API 서버. `/v1/healthcheck` 엔드포인트가 있어서 liveness/readiness probe로 사용 가능. 포트 4000.
