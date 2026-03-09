# 디버그 기록 — 컨테이너와 Kubernetes의 함정들

## CGO_ENABLED=0의 함의

`CGO_ENABLED=0`을 빼먹으면 바이너리가 glibc에 동적 링크된다. distroless에는 glibc가 없으므로 컨테이너 실행 시:

```
exec /api: no such file or directory
```

파일이 분명히 존재하는데 "no such file or directory"? 동적 링커(`ld-linux-x86-64.so.2`)를 찾지 못해서 발생하는 에러. 에러 메시지가 직관적이지 않아 처음 만나면 혼란스럽다.

일부 Go 라이브러리(예: `modernc.org/sqlite`)는 CGO가 필요하다. 그런 경우 distroless 대신 `alpine` 런타임을 써야 한다.

## COPY 경로와 빌드 컨텍스트

Dockerfile에서:
```dockerfile
COPY 01-backend-core/06-go-api-standard/go/go.mod ./go.mod
```

이 경로는 `docker build -f infra/Dockerfile ../..` 처럼 상위 디렉토리를 빌드 컨텍스트로 지정해야 동작한다. `docker build .`로 실행하면 경로를 찾지 못한다.

`.dockerignore`로 불필요한 파일을 제외해 빌드 컨텍스트 크기를 줄이는 것도 중요.

## Helm Template 검증

```bash
helm template go-backend charts/go-backend
```

이 명령으로 실제 Kubernetes에 배포하기 전에 생성될 YAML을 미리 확인할 수 있다. 템플릿 문법 오류, 잘못된 들여쓰기, 빠진 값 등을 사전에 발견.

```bash
helm lint charts/go-backend
```

차트 구조와 best practice 검증. `Chart.yaml` 필수 필드 누락 등을 체크.

## HPA와 resources 설정 관계

HPA가 CPU 기반으로 스케일 아웃하려면 Deployment에 `resources.requests.cpu`가 반드시 설정되어 있어야 한다. 미설정 시 metrics-server가 사용률을 계산할 수 없어 HPA가 동작하지 않는다.

## Secret 관리의 딜레마

Helm 차트에 `secret.yaml`이 있지만, 실제 비밀번호를 values.yaml에 평문으로 넣을 수 없다. 프로덕션에서는:
1. `helm-secrets` 플러그인 + SOPS로 암호화
2. External Secrets Operator로 Vault/AWS Secrets Manager에서 주입
3. ArgoCD Vault Plugin

이 프로젝트에서는 placeholder만 두고, 실 배포 시 `--set` 또는 sealed-secret으로 주입하는 방식.

## ArgoCD Sync 실패와 Retry

```yaml
retry:
  limit: 5
  backoff:
    duration: 5s
    factor: 2
    maxDuration: 3m
```

동기화 실패 시 5s → 10s → 20s → 40s → 80s 간격으로 최대 5번 재시도. CRD가 아직 설치되지 않았거나, PV 프로비저닝이 느린 경우에 유용.
