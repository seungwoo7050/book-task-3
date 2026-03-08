# Core Concepts

## 핵심 개념

- multi-stage Docker build는 빌드 환경과 런타임 환경을 분리한다.
- Helm chart는 manifest를 값 중심으로 재사용하게 만든다.
- ArgoCD Application은 “Git 상태를 클러스터에 동기화한다”는 선언적 모델이다.
- `verified` 최소 기준은 로컬에서 재현 가능한 `docker-build`, `helm-lint`, `helm-template`로 둔다.

## Trade-offs

- chart를 일반화할수록 values 구조가 복잡해진다.
- cluster apply까지 verified에 넣으면 로컬 환경 의존성이 너무 커진다.

## 실패하기 쉬운 지점

- Docker build context와 실제 소스 위치가 어긋나기 쉽다.
- Helm lint를 통과해도 values 조합에 따라 template render는 실패할 수 있다.

