# 16 GitOps Deploy — Helm Chart And Runtime Shape

`03-platform-engineering/16-gitops-deploy`는 Docker multi-stage build, Helm chart, ArgoCD manifest를 통해 코드 자산을 배포 자산으로 번역하는 인프라 과제다. 이 글에서는 4단계: Helm 템플릿 작성 -> 5단계: Helm 검증 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 4단계: Helm 템플릿 작성
- 5단계: Helm 검증

## Day 1
### Session 1

- 당시 목표: `01-backend-core/06-go-api-standard` 구현을 배포 대상으로 삼아 build context와 chart 구성을 보여 준다.
- 변경 단위: `deployment.yaml`, `service.yaml`, `configmap.yaml`, `secret.yaml`, `hpa.yaml`
- 처음 가설: 실제 클러스터 접속 대신 Docker/Helm/ArgoCD manifest 정합성 검증까지를 본선 범위로 제한했다.
- 실제 진행: 6개 파일: `_helpers.tpl` — 이름, 라벨, 셀렉터 헬퍼 `deployment.yaml` — Pod spec, 환경변수, 프로브, 리소스 `service.yaml` — ClusterIP, port 80 → targetPort 4000 `configmap.yaml` — PORT, ENV, LOG_LEVEL `secret.yaml` — DB 인증 정보 플레이스홀더 `hpa.yaml` — CPU 70%, Memory 80% 기준

CLI:

```bash
# 문법 검사
helm lint charts/go-backend

# 렌더링 결과 확인
helm template go-backend charts/go-backend

# 특정 값 오버라이드 테스트
helm template go-backend charts/go-backend --set replicaCount=5
```

검증 신호:

- helm lint charts/go-backend
- helm template go-backend charts/go-backend
- helm template go-backend charts/go-backend --set replicaCount=5

핵심 코드: `solution/infra/charts/go-backend/templates/deployment.yaml`

```yaml
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "go-backend.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "go-backend.selectorLabels" . | nindent 8 }}
      annotations:
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
```

왜 이 코드가 중요했는가:

이 설정은 이미지, probe, env, 리소스 같은 운영 기본값을 한 덩어리로 고정한다. Helm을 쓴 이유가 추상화가 아니라 재현 가능한 런타임 surface였다는 점이 여기서 드러난다.

새로 배운 것:

- Helm chart는 manifest를 값 중심으로 재사용하게 만든다.

보조 코드: `solution/infra/charts/go-backend/values.yaml`

```yaml
# Default values for go-backend.

replicaCount: 2

image:
  repository: ghcr.io/woopinbell/go-backend-api
  tag: "latest"
  pullPolicy: IfNotPresent

nameOverride: ""
fullnameOverride: ""

service:
  type: ClusterIP
  port: 80
  targetPort: 4000

resources:
  requests:
    cpu: 100m
```

왜 이 코드도 같이 봐야 하는가:

이 설정은 이미지, probe, env, 리소스 같은 운영 기본값을 한 덩어리로 고정한다. Helm을 쓴 이유가 추상화가 아니라 재현 가능한 런타임 surface였다는 점이 여기서 드러난다.

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

- 다음 글에서는 `30-argocd-and-infra-proof.md`에서 이어지는 경계를 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/infra/charts/go-backend/templates/deployment.yaml` 같은 결정적인 코드와 `make test-infra` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
