# 접근 기록 — Dockerfile에서 ArgoCD까지

## Dockerfile: 두 단계 빌드

### Build Stage

```dockerfile
FROM golang:1.22-alpine AS builder
RUN apk add --no-cache ca-certificates
WORKDIR /src
COPY go.mod ./go.mod
RUN go mod download
COPY . ./
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -o /out/api ./cmd/api
```

핵심 결정들:
- **`CGO_ENABLED=0`**: 순수 Go 바이너리. C 라이브러리 의존성 없음. distroless에 libc가 없어도 동작.
- **`-ldflags="-s -w"`**: 심볼 테이블(`-s`)과 DWARF 디버그 정보(`-w`) 제거. 바이너리 크기 30~40% 감소.
- **`ca-certificates`**: HTTPS 호출을 위한 루트 인증서. distroless에는 없으므로 빌더에서 복사.
- **`go mod download` 분리**: go.mod만 먼저 복사해 의존성을 캐시. 소스 변경 시 레이어 캐시 활용.

### Runtime Stage

```dockerfile
FROM gcr.io/distroless/static-debian12
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /out/api /api
EXPOSE 4000
USER nonroot:nonroot
ENTRYPOINT ["/api"]
```

- **distroless**: Shell, 패키지 매니저 없음. 공격 표면 최소화. 최종 이미지 ~20MB.
- **`USER nonroot:nonroot`**: 루트가 아닌 사용자로 실행. 컨테이너가 탈취당해도 권한 제한.

## Helm Chart: go-backend

### 구조

```
charts/go-backend/
├── Chart.yaml          # 메타데이터
├── values.yaml         # 기본 설정값
└── templates/
    ├── _helpers.tpl    # 공통 헬퍼 (이름 생성, 라벨)
    ├── deployment.yaml # Deployment
    ├── service.yaml    # ClusterIP Service
    ├── configmap.yaml  # 환경 변수
    ├── secret.yaml     # DB 인증 정보
    └── hpa.yaml        # HPA
```

### values.yaml 설계

기본값에서 곧바로 동작하도록 설계:
- `replicaCount: 2` — 가용성 기본 보장
- `image.repository: ghcr.io/woopinbell/go-backend-api`
- `resources.requests.memory: 64Mi`, `limits.memory: 128Mi` — Go 서비스에 적합한 최소 사양
- `autoscaling.enabled: true`, CPU 70%, Memory 80%에서 스케일 아웃
- liveness/readiness probe 경로: `/v1/healthcheck`

### _helpers.tpl

`{{ include "go-backend.fullname" . }}` 같은 공통 라벨/이름 생성 헬퍼. Helm 차트의 관례. `nameOverride`, `fullnameOverride`를 지원.

## ArgoCD Application

```yaml
spec:
  source:
    path: 03-platform-engineering/16-gitops-deploy/infra/charts/go-backend
    helm:
      valueFiles:
        - values.yaml
  syncPolicy:
    automated:
      prune: true      # Git에서 삭제된 리소스 클러스터에서도 삭제
      selfHeal: true    # 수동 변경(kubectl edit)을 Git 상태로 되돌림
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

`selfHeal: true`가 GitOps의 핵심. 누군가 `kubectl`로 리소스를 직접 수정해도 ArgoCD가 Git의 상태로 되돌린다.
