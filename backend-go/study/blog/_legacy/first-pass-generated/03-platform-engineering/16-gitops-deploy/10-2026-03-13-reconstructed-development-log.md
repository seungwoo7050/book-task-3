# 16 GitOps Deploy 재구성 개발 로그

16 GitOps Deploy는 Docker multi-stage build, Helm chart, ArgoCD manifest를 통해 코드 자산을 배포 자산으로 번역하는 인프라 과제다.

이 글은 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 쓴 버전이다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다. 세밀한 shell history가 남아 있지 않아 시간 표지는 `Phase 1/2/3`처럼 재구성했고, 근거는 README, 살아 있는 소스코드, docs, 테스트, 현재 CLI 재실행 결과만 사용했다.

## 구현 순서 요약

- Phase 1: multi-stage Dockerfile로 build, runtime 경계를 먼저 자른다 - `solution/infra/Dockerfile`의 `Dockerfile builder stage`
- Phase 2: Helm chart values와 templates로 배포 표면을 일반화한다 - `solution/infra/charts/go-backend/templates/deployment.yaml`의 `Helm Deployment template`
- Phase 3: ArgoCD manifest와 lint, template로 GitOps 검증선을 잠근다 - `solution/infra/k8s/argocd-app.yaml`의 `ArgoCD Application`

                ## Phase 1. multi-stage Dockerfile로 build, runtime 경계를 먼저 자른다

        - 당시 목표: multi-stage Dockerfile로 build, runtime 경계를 먼저 자른다
        - 변경 단위: `solution/infra/Dockerfile`의 `Dockerfile builder stage`
        - 처음 가설: `Dockerfile builder stage`처럼 build/runtime 경계를 먼저 자르지 않으면 뒤의 chart 값이 무엇을 배포하는지 흐려진다고 봤다.
        - 실제 진행: `solution/infra/Dockerfile`의 `Dockerfile builder stage`를 통해 build image와 runtime image가 분리되도록 자산 바닥을 먼저 깔았다.
        - CLI: `make -C problem helm-lint`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `helm lint ../solution/infra/charts/go-backend`였다.

        핵심 코드:

        ```
        FROM golang:1.22-alpine AS builder

RUN apk add --no-cache ca-certificates

WORKDIR /src

# Copy the target module only. This keeps the build aligned with the study tree
# instead of the legacy workspace.
COPY 01-backend-core/06-go-api-standard/solution/go/go.mod ./go.mod
        ```

        왜 이 코드가 중요했는가: `Dockerfile builder stage`는 `solution/infra/Dockerfile`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

        - 새로 배운 것: multi-stage Docker build는 빌드 환경과 런타임 환경을 분리한다.
        - 다음: Helm chart values와 templates로 배포 표면을 일반화한다
        ## Phase 2. Helm chart values와 templates로 배포 표면을 일반화한다

        - 당시 목표: Helm chart values와 templates로 배포 표면을 일반화한다
        - 변경 단위: `solution/infra/charts/go-backend/templates/deployment.yaml`의 `Helm Deployment template`
        - 처음 가설: `Helm Deployment template` 쪽에서 values와 template를 맞춰야 같은 chart를 여러 환경으로 확장할 수 있다고 판단했다.
        - 실제 진행: `solution/infra/charts/go-backend/templates/deployment.yaml`의 `Helm Deployment template`에서 values와 template 조합을 맞춰 deployment surface를 일반화했다.
        - CLI: `make -C problem helm-template`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `helm template go-backend ../solution/infra/charts/go-backend`였다.

        핵심 코드:

        ```yaml
        apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "go-backend.fullname" . }}
  labels:
    {{- include "go-backend.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
        ```

        왜 이 코드가 중요했는가: `Helm Deployment template`는 `solution/infra/charts/go-backend/templates/deployment.yaml`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

        - 새로 배운 것: cluster apply까지 verified에 넣으면 로컬 환경 의존성이 너무 커진다.
        - 다음: ArgoCD manifest와 lint, template로 GitOps 검증선을 잠근다
        ## Phase 3. ArgoCD manifest와 lint, template로 GitOps 검증선을 잠근다

        - 당시 목표: ArgoCD manifest와 lint, template로 GitOps 검증선을 잠근다
        - 변경 단위: `solution/infra/k8s/argocd-app.yaml`의 `ArgoCD Application`
        - 처음 가설: `ArgoCD Application`와 lint/template가 있어야 GitOps 자산이 로컬에서도 깨지지 않는다고 봤다.
        - 실제 진행: `solution/infra/k8s/argocd-app.yaml`의 `ArgoCD Application`와 helm lint, template를 묶어 GitOps asset 검증선을 로컬에서 닫았다.
        - CLI: `make -C problem helm-template`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `helm template go-backend ../solution/infra/charts/go-backend`였다.

        핵심 코드:

        ```yaml
        apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: go-backend
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
        ```

        왜 이 코드가 중요했는가: `ArgoCD Application`는 `solution/infra/k8s/argocd-app.yaml`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

        - 새로 배운 것: Helm lint를 통과해도 values 조합에 따라 template render는 실패할 수 있다.
        - 다음: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

                ## CLI 1. 현재 저장소에서 다시 돌린 검증

                ```bash
(cd /Users/woopinbell/work/book-task-3/study/03-platform-engineering/16-gitops-deploy && make -C problem helm-lint)
```

```text
helm lint ../solution/infra/charts/go-backend
==> Linting ../solution/infra/charts/go-backend
[INFO] Chart.yaml: icon is recommended
1 chart(s) linted, 0 chart(s) failed
```
        ## CLI 2. 현재 저장소에서 다시 돌린 검증

                ```bash
(cd /Users/woopinbell/work/book-task-3/study/03-platform-engineering/16-gitops-deploy && make -C problem helm-template)
```

```text
helm template go-backend ../solution/infra/charts/go-backend
---
# Source: go-backend/templates/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: go-backend
  labels:
    helm.sh/chart: go-backend-0.1.0
    app.kubernetes.io/name: go-backend
    app.kubernetes.io/instance: go-backend
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/managed-by: Helm
type: Opaque
data:
  # Base64-encoded placeholder values.
  # In production, use Sealed Secrets or External Secrets Operator.
  DATABASE_USER: "cm9vdA=="
  DATABASE_PASSWORD: ""
---
# Source: go-backend/templates/configmap.yaml
apiVersion: v1
... (136 more lines)
```

## 이번 재작성에서 남은 것

- 이번 글을 지탱한 개념 축: `multi-stage Docker build는 빌드 환경과 런타임 환경을 분리한다.`, `Helm chart는 manifest를 값 중심으로 재사용하게 만든다.`, `ArgoCD Application은 “Git 상태를 클러스터에 동기화한다”는 선언적 모델이다.`, verified` 최소 기준은 로컬에서 재현 가능한 `docker-build`, `helm-lint`, `helm-template`로 둔다.
- 최신 검증 메모: 현재 저장소에서 다시 실행한 명령은 모두 exit 0으로 끝났다.
- 다음 질문: Go API 한 개를 Docker image, Helm chart, ArgoCD Application으로 번역한다.
