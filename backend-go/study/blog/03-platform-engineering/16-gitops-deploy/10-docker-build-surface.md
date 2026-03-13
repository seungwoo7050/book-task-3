# 16 GitOps Deploy — Docker Build Surface

`03-platform-engineering/16-gitops-deploy`는 Docker multi-stage build, Helm chart, ArgoCD manifest를 통해 코드 자산을 배포 자산으로 번역하는 인프라 과제다. 이 글에서는 1단계: Dockerfile 작성 -> 2단계: .dockerignore 작성 -> 3단계: Helm Chart 스캐폴딩 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 1단계: Dockerfile 작성
- 2단계: .dockerignore 작성
- 3단계: Helm Chart 스캐폴딩

## Day 1
### Session 1

- 당시 목표: Go 서비스용 multi-stage Dockerfile을 작성해야 한다.
- 변경 단위: `**/*_test.go`
- 처음 가설: 학습 포인트를 배포 자산 자체에 두기 위해 단일 서비스 배포 기준선만 다룬다.
- 실제 진행: Dockerfile 작성: 빌드 테스트: 빌드 컨텍스트 크기 감소 → 빌드 속도 향상. Chart.yaml

CLI:

```bash
cd 16-gitops-deploy/infra

# 빌드 컨텍스트를 study/ 루트로 설정
docker build -f solution/infra/Dockerfile -t go-backend-api:dev ../../

# 이미지 크기 확인
docker images go-backend-api:dev
# ~15-20MB

# 실행 테스트
docker run -p 4000:4000 go-backend-api:dev
```

검증 신호:

- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.

핵심 코드: `solution/infra/Dockerfile`

```dockerfile
FROM golang:1.22-alpine AS builder

RUN apk add --no-cache ca-certificates

WORKDIR /src

# Copy the target module only. This keeps the build aligned with the study tree
# instead of the legacy workspace.
COPY 01-backend-core/06-go-api-standard/solution/go/go.mod ./go.mod
RUN go mod download

COPY 01-backend-core/06-go-api-standard/solution/go/ ./

RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
	-ldflags="-s -w" \
	-o /out/api ./cmd/api

FROM gcr.io/distroless/static-debian12
```

왜 이 코드가 중요했는가:

이 블록은 애플리케이션 코드가 실제 배포 가능한 이미지로 축약되는 경계를 보여 준다. 멀티 스테이지를 어떻게 잡았는지가 곧 이 프로젝트의 핵심 구현 판단이다.

새로 배운 것:

- multi-stage Docker build는 빌드 환경과 런타임 환경을 분리한다.

보조 코드: `solution/README.md`

```text
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
```

왜 이 코드도 같이 봐야 하는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

CLI:

```bash
make test-infra
```

검증 신호:

- 2026-03-07 기준 `make test-infra`가 통과했다.
- `docker-build`는 `01-backend-core/06-go-api-standard/go` 모듈을 multi-stage Dockerfile로 이미지 빌드했다.
- `helm-lint`는 chart 구조 오류 없이 통과했고, `helm template`은 `Deployment`, `Service`, `ConfigMap`, `Secret`, `HPA`를 정상 렌더링했다.
- Helm 4.1.1은 Homebrew로 설치해 사용했다.

다음:

- 다음 글에서는 `20-helm-chart-and-runtime-shape.md`에서 이어지는 경계를 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/infra/Dockerfile` 같은 결정적인 코드와 `make test-infra` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
