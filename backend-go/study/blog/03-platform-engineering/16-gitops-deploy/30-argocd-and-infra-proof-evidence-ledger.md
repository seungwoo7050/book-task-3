# 16 GitOps Deploy Evidence Ledger

## 30 argocd-and-infra-proof

- 시간 표지: 6단계: ArgoCD Application 매니페스트 -> 7단계: 전체 빌드 검증
- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `k8s/argocd-app.yaml`
- 처음 가설: 실제 클러스터 접속 대신 Docker/Helm/ArgoCD manifest 정합성 검증까지를 본선 범위로 제한했다.
- 실제 조치: `k8s/argocd-app.yaml` 작성: `source.path`: 차트 디렉토리 `syncPolicy.automated.prune: true` `syncPolicy.automated.selfHeal: true` `retry.limit: 5` + exponential backoff

CLI:

```bash
mkdir -p k8s

# Makefile 타겟 사용
make -C problem docker-build
make -C problem helm-lint
make -C problem helm-template
```

- 검증 신호:
- make -C problem helm-lint
- make -C problem helm-template
- 2026-03-07 기준 `make test-infra`가 통과했다.
- `docker-build`는 `01-backend-core/06-go-api-standard/go` 모듈을 multi-stage Dockerfile로 이미지 빌드했다.
- `helm-lint`는 chart 구조 오류 없이 통과했고, `helm template`은 `Deployment`, `Service`, `ConfigMap`, `Secret`, `HPA`를 정상 렌더링했다.
- 핵심 코드 앵커: `solution/infra/k8s/argocd-app.yaml`
- 새로 배운 것: ArgoCD Application은 “Git 상태를 클러스터에 동기화한다”는 선언적 모델이다.
- 다음: `helm upgrade --install`과 `kubectl apply -f ../solution/infra/k8s/argocd-app.yaml`는 로컬 클러스터가 있을 때만 추가 검증한다.
