# 회고 — 인프라를 코드로 다룬다는 것

## Go 코드가 하나도 없는 프로젝트

이 프로젝트에서는 Go 코드를 한 줄도 작성하지 않았다. 하지만 이전 프로젝트들에서 만든 Go 서비스가 "실제로 동작하는 서비스"가 되려면 이 단계가 필수다.

Dockerfile, Helm Chart, ArgoCD Manifest — 세 가지 모두 선언적(declarative) 포맷이다. "이렇게 해라"가 아니라 "이 상태여야 한다"를 기술한다. Go 코드가 "어떻게(how)"를 다루는 것과 대조적이다.

## 멀티 스테이지 빌드의 가치

빌드 도구(Go 컴파일러, apk 패키지)가 최종 이미지에 포함되지 않는다. 1GB+ 빌드 이미지에서 ~20MB 런타임 이미지를 얻는다. 보안(공격 표면 축소)과 배포 속도(이미지 풀 시간) 모두에서 이득.

distroless를 선택한 이유: alpine보다 더 작고, shell이 없어서 `docker exec` 침투도 불가. 대신 디버깅이 어렵다. 필요하면 [distroless/debug](https://github.com/GoogleContainerTools/distroless/tree/main/debug) 이미지를 사용.

## Helm vs Kustomize

Helm은 Go 템플릿 기반으로 변수를 주입한다. Kustomize는 패치 기반으로 YAML을 오버레이한다.

이 프로젝트에서 Helm을 선택한 이유:
1. 커뮤니티 차트 생태계가 더 큼
2. `values.yaml`로 환경별 설정 관리가 직관적
3. ArgoCD가 Helm을 네이티브 지원

Kustomize가 더 나은 경우: 차트 형태가 아닌 raw YAML을 관리할 때, 패치(overlay)가 더 읽기 쉬울 때.

## GitOps의 핵심: Self-Heal

`selfHeal: true`가 이 프로젝트에서 가장 중요한 한 줄이다. 이것이 없으면 GitOps가 아니라 그냥 "Git에서 배포"다. 누군가 `kubectl scale deployment --replicas=1`을 실행해도, ArgoCD가 Git의 `replicaCount: 2`로 복원한다.

이것은 운영 규칙이기도 하다: 클러스터에 직접 변경을 가하지 말라. 모든 변경은 Git을 통해.

## 다음에 다시 만든다면

GitHub Actions 워크플로를 추가할 것이다. PR → 테스트 → Docker 빌드 → GHCR 푸시 → values.yaml 이미지 태그 업데이트 → ArgoCD 자동 동기화. 현재 프로젝트에서 CI 파이프라인은 스코프 밖이지만, GitOps의 완성은 CI와 CD의 연결이다.
