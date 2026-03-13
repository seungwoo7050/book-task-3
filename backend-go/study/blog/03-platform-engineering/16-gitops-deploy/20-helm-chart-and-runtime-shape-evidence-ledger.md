# 16 GitOps Deploy Evidence Ledger

## 20 helm-chart-and-runtime-shape

- 시간 표지: 4단계: Helm 템플릿 작성 -> 5단계: Helm 검증
- 당시 목표: `01-backend-core/06-go-api-standard` 구현을 배포 대상으로 삼아 build context와 chart 구성을 보여 준다.
- 변경 단위: `deployment.yaml`, `service.yaml`, `configmap.yaml`, `secret.yaml`, `hpa.yaml`
- 처음 가설: 실제 클러스터 접속 대신 Docker/Helm/ArgoCD manifest 정합성 검증까지를 본선 범위로 제한했다.
- 실제 조치: 6개 파일: `_helpers.tpl` — 이름, 라벨, 셀렉터 헬퍼 `deployment.yaml` — Pod spec, 환경변수, 프로브, 리소스 `service.yaml` — ClusterIP, port 80 → targetPort 4000 `configmap.yaml` — PORT, ENV, LOG_LEVEL `secret.yaml` — DB 인증 정보 플레이스홀더 `hpa.yaml` — CPU 70%, Memory 80% 기준

CLI:

```bash
# 문법 검사
helm lint charts/go-backend

# 렌더링 결과 확인
helm template go-backend charts/go-backend

# 특정 값 오버라이드 테스트
helm template go-backend charts/go-backend --set replicaCount=5
```

- 검증 신호:
- helm lint charts/go-backend
- helm template go-backend charts/go-backend
- helm template go-backend charts/go-backend --set replicaCount=5
- 핵심 코드 앵커: `solution/infra/charts/go-backend/templates/deployment.yaml`
- 새로 배운 것: Helm chart는 manifest를 값 중심으로 재사용하게 만든다.
- 다음: 다음 글에서는 `30-argocd-and-infra-proof.md`에서 이어지는 경계를 다룬다.
