# Problem: Realtime Chat

> Status: VERIFIED
> Scope: local-first chat model
> Last Checked: 2026-03-12

## 문제 요약

offline send, ack reconcile, replay from `lastEventId`, typing/presence update를
하나의 local-first message model로 검증하는 채팅 과제다.

## 왜 이 문제가 커리큘럼에 필요한가

offline sync 규칙을 배운 다음에는 그 규칙을 제품형 상호작용 안에 넣어야 한다.
이 프로젝트는 "실시간 채팅이라는 사용자 경험을 유지하면서도 duplicate-safe replay를 설명할 수 있는가"를 묻는다.

## 제공 자료

- 기존 realtime-chat 과제 요구사항
- `problem/code/README.md`의 참고 코드
- `problem/data/README.md`의 fixture 설명

## 필수 요구사항

1. pending message creation
2. server ack reconciliation
3. replay dedupe
4. typing and presence update
5. local-first storage schema

## 의도적 비범위

- production websocket infra
- 다중 기기 동기화 충돌 해결
- push notification delivery

## 평가/검증 기준

```bash
make test
make app-build
make app-test
```

- offline send와 ack reconcile이 같은 message lifecycle을 공유해야 한다.
- replay 시 duplicate event를 걸러야 한다.
- schema와 UI 동작이 같은 모델 설명으로 이어져야 한다.

## 원문/출처 보존 위치

- [SOURCE-PROVENANCE.md](SOURCE-PROVENANCE.md)
- [code/README.md](code/README.md)
- [data/README.md](data/README.md)
