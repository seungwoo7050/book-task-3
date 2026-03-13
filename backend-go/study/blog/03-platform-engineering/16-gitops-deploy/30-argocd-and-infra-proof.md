# 16 GitOps Deploy — Argocd And Infra Proof

`03-platform-engineering/16-gitops-deploy`는 Docker multi-stage build, Helm chart, ArgoCD manifest를 통해 코드 자산을 배포 자산으로 번역하는 인프라 과제다. 이 글에서는 6단계: ArgoCD Application 매니페스트 -> 7단계: 전체 빌드 검증 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 6단계: ArgoCD Application 매니페스트
- 7단계: 전체 빌드 검증

## Day 1
### Session 1

- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `k8s/argocd-app.yaml`
- 처음 가설: 실제 클러스터 접속 대신 Docker/Helm/ArgoCD manifest 정합성 검증까지를 본선 범위로 제한했다.
- 실제 진행: `k8s/argocd-app.yaml` 작성: `source.path`: 차트 디렉토리 `syncPolicy.automated.prune: true` `syncPolicy.automated.selfHeal: true` `retry.limit: 5` + exponential backoff

CLI:

```bash
mkdir -p k8s

# Makefile 타겟 사용
make -C problem docker-build
make -C problem helm-lint
make -C problem helm-template
```

검증 신호:

- make -C problem helm-lint
- make -C problem helm-template
- 2026-03-07 기준 `make test-infra`가 통과했다.
- `docker-build`는 `01-backend-core/06-go-api-standard/go` 모듈을 multi-stage Dockerfile로 이미지 빌드했다.
- `helm-lint`는 chart 구조 오류 없이 통과했고, `helm template`은 `Deployment`, `Service`, `ConfigMap`, `Secret`, `HPA`를 정상 렌더링했다.

핵심 코드: `solution/infra/k8s/argocd-app.yaml`

```yaml
spec:
  project: default

  source:
    repoURL: https://github.com/<your-org>/<your-repo>.git
    targetRevision: main
    path: 03-platform-engineering/16-gitops-deploy/solution/infra/charts/go-backend

    helm:
      valueFiles:
        - values.yaml

  destination:
    server: https://kubernetes.default.svc
    namespace: default

  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

왜 이 코드가 중요했는가:

이 매니페스트는 Git에 적은 원하는 상태가 실제 동기화 정책으로 내려오는 지점이다. 선언적 배포라는 말을 코드 밖이 아니라 YAML 안에서 증명해 준다.

새로 배운 것:

- ArgoCD Application은 “Git 상태를 클러스터에 동기화한다”는 선언적 모델이다.

보조 코드: `solution/infra/charts/go-backend/templates/hpa.yaml`

```yaml
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ include "go-backend.fullname" . }}
  minReplicas: {{ .Values.autoscaling.minReplicas }}
  maxReplicas: {{ .Values.autoscaling.maxReplicas }}
  metrics:
    {{- if .Values.autoscaling.targetCPUUtilizationPercentage }}
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: {{ .Values.autoscaling.targetCPUUtilizationPercentage }}
    {{- end }}
    {{- if .Values.autoscaling.targetMemoryUtilizationPercentage }}
    - type: Resource
      resource:
        name: memory
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

- `helm upgrade --install`과 `kubectl apply -f ../solution/infra/k8s/argocd-app.yaml`는 로컬 클러스터가 있을 때만 추가 검증한다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/infra/k8s/argocd-app.yaml` 같은 결정적인 코드와 `make test-infra` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
