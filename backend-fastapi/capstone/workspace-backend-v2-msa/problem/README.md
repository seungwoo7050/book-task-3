# 문제 정의

## 문제

`workspace-backend` v1은 인증, 워크스페이스 도메인, 알림 전달을 한 프로세스 안에서 통합했다. v2의 목표는 같은 협업형 도메인을 MSA로 다시 분해해, public API를 유지한 채 내부 경계와 분산 복잡성이 어떻게 바뀌는지 설명 가능한 상태로 만드는 것이다.

## 성공 기준

- `gateway`가 public `/api/v1/auth/*`, `/api/v1/platform/*` 경로를 유지해야 한다.
- `identity-service`, `workspace-service`, `notification-service`는 각자 자기 DB만 읽어야 한다.
- 댓글 생성은 outbox에 기록되고, 이후 stream consumer와 websocket fan-out으로 이어져야 한다.
- notification-service가 잠시 내려가도 댓글 생성은 성공하고, 복구 후 consume로 알림이 전달되어야 한다.
- v1과 v2의 차이를 문서와 노트만 읽고 설명할 수 있어야 한다.

## canonical verification 시작 위치

- 실행과 검증 진입점은 [../fastapi/README.md](../fastapi/README.md)입니다.

## 제외 범위

- Kubernetes, service mesh, service discovery
- 실제 클라우드 배포 자동화와 IaC
- front-end 렌더링과 정적 자산
- saga orchestration과 다단계 보상 흐름
