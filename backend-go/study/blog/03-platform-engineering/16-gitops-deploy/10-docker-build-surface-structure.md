# 16 GitOps Deploy Structure

## 이 글이 답할 질문

- Go 서비스용 multi-stage Dockerfile을 작성해야 한다.
- 학습 포인트를 배포 자산 자체에 두기 위해 단일 서비스 배포 기준선만 다룬다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `03-platform-engineering/16-gitops-deploy` 안에서 `10-docker-build-surface.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 1단계: Dockerfile 작성 -> 2단계: .dockerignore 작성 -> 3단계: Helm Chart 스캐폴딩
- 세션 본문: `**/*_test.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/infra/Dockerfile`
- 코드 앵커 2: `solution/README.md`
- 코드 설명 초점: 이 블록은 애플리케이션 코드가 실제 배포 가능한 이미지로 축약되는 경계를 보여 준다. 멀티 스테이지를 어떻게 잡았는지가 곧 이 프로젝트의 핵심 구현 판단이다.
- 개념 설명: multi-stage Docker build는 빌드 환경과 런타임 환경을 분리한다.
- 마지막 단락: 다음 글에서는 `20-helm-chart-and-runtime-shape.md`에서 이어지는 경계를 다룬다.
