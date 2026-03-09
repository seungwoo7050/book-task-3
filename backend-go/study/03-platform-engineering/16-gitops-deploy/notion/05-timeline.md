# 타임라인 — GitOps 배포 프로젝트 전체 과정

## 1단계: Dockerfile 작성

```bash
cd 16-gitops-deploy/infra
```

Dockerfile 작성:

```dockerfile
# Build: golang:1.22-alpine
# Runtime: gcr.io/distroless/static-debian12
```

빌드 테스트:

```bash
# 빌드 컨텍스트를 study/ 루트로 설정
docker build -f infra/Dockerfile -t go-backend-api:dev ../../

# 이미지 크기 확인
docker images go-backend-api:dev
# ~15-20MB

# 실행 테스트
docker run -p 4000:4000 go-backend-api:dev
```

## 2단계: .dockerignore 작성

```
.git/
node_modules/
*.md
docs/
devlog/
*_test.go
**/*_test.go
```

빌드 컨텍스트 크기 감소 → 빌드 속도 향상.

## 3단계: Helm Chart 스캐폴딩

```bash
# Helm CLI로 차트 생성 (또는 수동 작성)
helm create charts/go-backend

# 불필요한 기본 파일 정리 후 커스터마이징
```

### Chart.yaml

```yaml
apiVersion: v2
name: go-backend
version: 0.1.0
appVersion: "1.0.0"
```

### values.yaml 설계

```yaml
replicaCount: 2
image:
  repository: ghcr.io/woopinbell/go-backend-api
  tag: "latest"
resources:
  requests: { cpu: 100m, memory: 64Mi }
  limits:   { cpu: 500m, memory: 128Mi }
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
probes:
  liveness:  { path: /v1/healthcheck }
  readiness: { path: /v1/healthcheck }
```

## 4단계: Helm 템플릿 작성

6개 파일:
- `_helpers.tpl` — 이름, 라벨, 셀렉터 헬퍼
- `deployment.yaml` — Pod spec, 환경변수, 프로브, 리소스
- `service.yaml` — ClusterIP, port 80 → targetPort 4000
- `configmap.yaml` — PORT, ENV, LOG_LEVEL
- `secret.yaml` — DB 인증 정보 placeholder
- `hpa.yaml` — CPU 70%, Memory 80% 기준

## 5단계: Helm 검증

```bash
# 문법 검사
helm lint charts/go-backend

# 렌더링 결과 확인
helm template go-backend charts/go-backend

# 특정 값 오버라이드 테스트
helm template go-backend charts/go-backend --set replicaCount=5
```

## 6단계: ArgoCD Application 매니페스트

```bash
mkdir -p k8s
```

`k8s/argocd-app.yaml` 작성:
- `source.path`: 차트 디렉토리
- `syncPolicy.automated.prune: true`
- `syncPolicy.automated.selfHeal: true`
- `retry.limit: 5` + exponential backoff

## 7단계: 전체 빌드 검증

```bash
# Makefile 타겟 사용
make -C problem docker-build
make -C problem helm-lint
make -C problem helm-template
```

## 소스 코드에서 보이지 않는 것들

| 항목 | 설명 |
|------|------|
| Docker 빌드 컨텍스트 | `../../` (study/ 루트) — Dockerfile이 다른 프로젝트의 소스를 참조 |
| distroless 이미지 선택 | `static-debian12` — glibc 없는 가장 작은 변종 |
| 이미지 레지스트리 | `ghcr.io` (GitHub Container Registry) — 기본값, 실 배포 시 변경 |
| Helm 버전 | Chart API v2 — Helm 3 전용 |
| ArgoCD 네임스페이스 | Application CRD는 `argocd` 네임스페이스에, 배포 대상은 `default` |
| Probe 타이밍 | liveness: 5s 후 시작 / readiness: 3s 후 시작 — Go 서버 기본 기동 시간 고려 |
| Secret 처리 | values.yaml에 placeholder만. 프로덕션에서는 sealed-secrets 또는 External Secrets |
| Kubernetes 미설치 | 로컬 클러스터(kind, minikube) 설치는 이 프로젝트 스코프 밖 |
| ArgoCD 설치 | `kubectl apply -n argocd -f https://...` 도 스코프 밖 |
