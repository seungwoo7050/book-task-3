# 16 GitOps Deploy Structure

## 이 글이 답할 질문

- `01-backend-core/06-go-api-standard` 구현을 배포 대상으로 삼아 build context와 chart 구성을 보여 준다.
- 실제 클러스터 접속 대신 Docker/Helm/ArgoCD manifest 정합성 검증까지를 본선 범위로 제한했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `03-platform-engineering/16-gitops-deploy` 안에서 `20-helm-chart-and-runtime-shape.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 4단계: Helm 템플릿 작성 -> 5단계: Helm 검증
- 세션 본문: `deployment.yaml, service.yaml, configmap.yaml, secret.yaml` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/infra/charts/go-backend/templates/deployment.yaml`
- 코드 앵커 2: `solution/infra/charts/go-backend/values.yaml`
- 코드 설명 초점: 이 설정은 이미지, probe, env, 리소스 같은 운영 기본값을 한 덩어리로 고정한다. Helm을 쓴 이유가 추상화가 아니라 재현 가능한 런타임 surface였다는 점이 여기서 드러난다.
- 개념 설명: Helm chart는 manifest를 값 중심으로 재사용하게 만든다.
- 마지막 단락: 다음 글에서는 `30-argocd-and-infra-proof.md`에서 이어지는 경계를 다룬다.
