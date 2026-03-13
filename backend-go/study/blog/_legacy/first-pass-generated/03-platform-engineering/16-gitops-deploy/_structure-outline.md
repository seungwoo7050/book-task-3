# 16 GitOps Deploy Structure Outline

이 문서는 chronology ledger를 바탕으로 최종 blog를 어떤 순서로 전개할지 먼저 고정한 설계 메모다. 기존 `blog/` 초안은 입력에서 제외했고, 실제 코드, README, docs, 테스트, CLI만을 근거로 삼는다.

## Planned Files

- `00-series-map.md`: 프로젝트 범위, source-of-truth, 읽는 순서를 잡는 진입 문서
- `01-evidence-ledger.md`: 파일, 함수, CLI 단위 chronology를 거칠게 복원한 근거 문서
- `10-2026-03-13-reconstructed-development-log.md`: 구현 순서와 판단 전환점을 세션 흐름으로 다시 쓴 최종 blog

## Final Blog Flow

- 도입: README 한 줄 요약과 이번 재검증 범위를 붙여 글의 위치를 먼저 밝힌다.
- 구현 순서 요약: Phase 1 -> Phase 2 -> Phase 3 순서를 미리 보여 준다.
- 세션형 chronology: 각 phase에서 당시 목표, 가설, 조치, 코드 앵커, 검증 신호를 순서대로 다시 적는다.
- CLI로 닫는 구간: 현재 저장소에서 다시 실행한 명령과 excerpt를 붙여 README 계약이 아직 살아 있는지 확인한다.
- 남은 질문: 개념 축과 다음 실험 지점을 남긴다.

## Section Plan

### 1. Phase 1 - multi-stage Dockerfile로 build, runtime 경계를 먼저 자른다

- 목표: multi-stage Dockerfile로 build, runtime 경계를 먼저 자른다
- 변경 단위: `solution/infra/Dockerfile`의 `Dockerfile builder stage`
- 핵심 가설: `Dockerfile builder stage`처럼 build/runtime 경계를 먼저 자르지 않으면 뒤의 chart 값이 무엇을 배포하는지 흐려진다고 봤다.
- 반드시 넣을 코드 앵커: `Dockerfile builder stage`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `helm lint ../solution/infra/charts/go-backend`였다.
- 새로 배운 것 섹션 포인트: multi-stage Docker build는 빌드 환경과 런타임 환경을 분리한다.
- 다음 섹션 연결 문장: Helm chart values와 templates로 배포 표면을 일반화한다
### 2. Phase 2 - Helm chart values와 templates로 배포 표면을 일반화한다

- 목표: Helm chart values와 templates로 배포 표면을 일반화한다
- 변경 단위: `solution/infra/charts/go-backend/templates/deployment.yaml`의 `Helm Deployment template`
- 핵심 가설: `Helm Deployment template` 쪽에서 values와 template를 맞춰야 같은 chart를 여러 환경으로 확장할 수 있다고 판단했다.
- 반드시 넣을 코드 앵커: `Helm Deployment template`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `helm template go-backend ../solution/infra/charts/go-backend`였다.
- 새로 배운 것 섹션 포인트: cluster apply까지 verified에 넣으면 로컬 환경 의존성이 너무 커진다.
- 다음 섹션 연결 문장: ArgoCD manifest와 lint, template로 GitOps 검증선을 잠근다
### 3. Phase 3 - ArgoCD manifest와 lint, template로 GitOps 검증선을 잠근다

- 목표: ArgoCD manifest와 lint, template로 GitOps 검증선을 잠근다
- 변경 단위: `solution/infra/k8s/argocd-app.yaml`의 `ArgoCD Application`
- 핵심 가설: `ArgoCD Application`와 lint/template가 있어야 GitOps 자산이 로컬에서도 깨지지 않는다고 봤다.
- 반드시 넣을 코드 앵커: `ArgoCD Application`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `helm template go-backend ../solution/infra/charts/go-backend`였다.
- 새로 배운 것 섹션 포인트: Helm lint를 통과해도 values 조합에 따라 template render는 실패할 수 있다.
- 다음 섹션 연결 문장: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

## Fixed CLI Anchor

        ```bash
(cd /Users/woopinbell/work/book-task-3/study/03-platform-engineering/16-gitops-deploy && make -C problem helm-lint)
```

```text
helm lint ../solution/infra/charts/go-backend
==> Linting ../solution/infra/charts/go-backend
[INFO] Chart.yaml: icon is recommended
1 chart(s) linted, 0 chart(s) failed
```

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
