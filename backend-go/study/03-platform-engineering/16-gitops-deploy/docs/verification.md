# Verification

## Commands

```bash
make test-infra
```

## Result

- 2026-03-07 기준 `make test-infra`가 통과했다.
- `docker-build`는 `01-backend-core/06-go-api-standard/go` 모듈을 multi-stage Dockerfile로 이미지 빌드했다.
- `helm-lint`는 chart 구조 오류 없이 통과했고, `helm template`은 `Deployment`, `Service`, `ConfigMap`, `Secret`, `HPA`를 정상 렌더링했다.
- Helm 4.1.1은 Homebrew로 설치해 사용했다.

## Remaining Checks

- `helm upgrade --install`과 `kubectl apply -f ../infra/k8s/argocd-app.yaml`는 로컬 클러스터가 있을 때만 추가 검증한다.
