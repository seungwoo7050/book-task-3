# 16 GitOps Deploy Structure

## 이 글이 답할 질문

- 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 실제 클러스터 접속 대신 Docker/Helm/ArgoCD manifest 정합성 검증까지를 본선 범위로 제한했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `03-platform-engineering/16-gitops-deploy` 안에서 `30-argocd-and-infra-proof.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 6단계: ArgoCD Application 매니페스트 -> 7단계: 전체 빌드 검증
- 세션 본문: `k8s/argocd-app.yaml` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/infra/k8s/argocd-app.yaml`
- 코드 앵커 2: `solution/infra/charts/go-backend/templates/hpa.yaml`
- 코드 설명 초점: 이 매니페스트는 Git에 적은 원하는 상태가 실제 동기화 정책으로 내려오는 지점이다. 선언적 배포라는 말을 코드 밖이 아니라 YAML 안에서 증명해 준다.
- 개념 설명: ArgoCD Application은 “Git 상태를 클러스터에 동기화한다”는 선언적 모델이다.
- 마지막 단락: `helm upgrade --install`과 `kubectl apply -f ../solution/infra/k8s/argocd-app.yaml`는 로컬 클러스터가 있을 때만 추가 검증한다.
