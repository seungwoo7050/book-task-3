# 16 GitOps Deploy

## 한 줄 요약

Docker multi-stage build, Helm chart, ArgoCD manifest를 통해 코드 자산을 배포 자산으로 번역하는 인프라 과제다.

## 이 프로젝트가 푸는 문제

- Go 서비스용 multi-stage Dockerfile을 작성해야 한다.
- Helm chart와 ArgoCD application manifest를 만들어야 한다.
- 코드 변경과 Git 기반 배포 변경의 경계를 설명해야 한다.

## 내가 만든 답

- Dockerfile, Helm chart, ArgoCD manifest를 `solution/infra`에 구성했다.
- `01-backend-core/06-go-api-standard` 구현을 배포 대상으로 삼아 build context와 chart 구성을 보여 준다.
- cluster apply는 제외하고 lint와 template, docker build까지를 canonical 검증으로 묶는다.

## 핵심 설계 선택

- 학습 포인트를 배포 자산 자체에 두기 위해 단일 서비스 배포 기준선만 다룬다.
- 실제 클러스터 접속 대신 Docker/Helm/ArgoCD manifest 정합성 검증까지를 본선 범위로 제한했다.

## 검증

- `make -C problem docker-build`
- `make -C problem helm-lint`
- `make -C problem helm-template`

## 제외 범위

- 실제 cluster apply
- ArgoCD sync smoke test

## 읽는 순서

1. [problem/README.md](problem/README.md)에서 canonical 문제 정의와 성공 기준을 읽는다.
2. [solution/README.md](solution/README.md)에서 구현 범위와 검증 진입점을 확인한다.
3. [docs/README.md](docs/README.md)에서 개념 설명과 참고 문서를 따라간다.
4. [notion/README.md](notion/README.md)에서 접근 로그, 디버그 기록, 회고를 확인한다.

## 상태

- 상태: `verified`
- 제공 자료와 provenance: legacy/03-platform-engineering/08-gitops-deploy (`legacy/03-platform-engineering/08-gitops-deploy/README.md`, public repo에는 미포함)
