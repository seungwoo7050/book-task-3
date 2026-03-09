# 지식 인덱스 — GitOps 배포에서 다룬 개념들

## Multi-Stage Build

Dockerfile에서 여러 FROM을 사용해 빌드 환경과 런타임 환경을 분리. `AS builder`로 이름 붙인 빌드 스테이지에서 컴파일하고, 최종 스테이지에 바이너리만 `COPY --from=builder`로 복사. 빌드 도구가 최종 이미지에 포함되지 않음.

## Distroless Image

Google이 관리하는 최소 컨테이너 이미지. Shell, 패키지 매니저, libc까지 없는 `static` 변종이 가장 작음. `gcr.io/distroless/static-debian12` 사용. 보안: 공격 표면 최소화. 제약: shell 디버깅 불가.

## CGO_ENABLED=0

Go 빌드 시 C 바인딩을 비활성화하는 환경 변수. 정적 바이너리를 생성해 어떤 Linux 환경에서든 glibc 없이 실행 가능. distroless, scratch 이미지와 함께 사용.

## Helm Chart

Kubernetes 리소스의 패키지 매니저. Chart.yaml(메타데이터), values.yaml(설정값), templates/(Go 템플릿 기반 YAML). `helm install`, `helm upgrade`, `helm rollback`으로 릴리스 관리.

## ArgoCD

Kubernetes용 GitOps CD 도구. Git 리포지토리의 선언적 설정과 클러스터 상태를 지속적으로 비교(reconcile). 차이가 있으면 자동 동기화(`automated.prune`, `automated.selfHeal`).

## Self-Heal

ArgoCD의 기능. 클러스터 리소스가 Git의 원하는 상태와 다르면 자동으로 복원. `kubectl`로 직접 변경해도 Git 상태로 되돌아감. GitOps의 핵심 원칙.

## Horizontal Pod Autoscaler (HPA)

Kubernetes에서 Pod 수를 자동으로 조정하는 리소스. CPU/Memory 사용률 기반. `resources.requests`가 설정되어 있어야 metrics-server가 사용률을 계산 가능. `targetCPUUtilizationPercentage: 70`이면 평균 70% 초과 시 스케일 아웃.

## Readiness / Liveness Probe

Kubernetes가 Pod의 상태를 판단하는 헬스체크. Liveness: 실패 시 Pod 재시작. Readiness: 실패 시 Service에서 제외(트래픽 차단). HTTP GET `/v1/healthcheck` 사용.

## ldflags "-s -w"

Go 링커 플래그. `-s`: 심볼 테이블 제거. `-w`: DWARF 디버그 정보 제거. 바이너리 크기를 30~40% 줄임. 프로덕션 빌드에서 일반적.

## .dockerignore

Docker 빌드 컨텍스트에서 제외할 파일/디렉토리 패턴. `.git/`, `*.md`, `docs/` 등을 제외해 빌드 컨텍스트 전송 시간과 레이어 캐시 무효화를 줄임.

## PruneLast

ArgoCD syncOption. 리소스 삭제를 동기화의 마지막에 수행. ConfigMap 교체 시 새 ConfigMap이 먼저 생성된 후 이전 것이 삭제됨. 배포 중 설정 참조가 끊기지 않음.
