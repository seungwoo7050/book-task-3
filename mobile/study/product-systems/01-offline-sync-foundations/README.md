# Offline Sync Foundations

Status: verified

## 한 줄 답

outbox, retry, DLQ, idempotency, conflict merge를 채팅 앱 전에 독립적으로 학습하기 위해 만든 offline sync 브리지 프로젝트다.

## 무슨 문제를 풀었나

local-first 제품은 곧바로 채팅 앱이나 캡스톤에 들어가면 변수 수가 너무 많아진다.
이 프로젝트의 질문은 "queue/retry/replay 규칙만 따로 떼어 deterministic하게 검증할 수 있는가"다.

## 내가 만든 답

- deterministic fake sync service를 만들었다.
- create queue, retry, DLQ, reconnect flush 규칙을 구현했다.
- idempotency와 conflict merge helper를 분리했다.
- 이후 프로젝트에서 재사용할 offline-first 개념을 문서로 고정했다.

## 무엇이 동작하나

- task create queue
- retry / DLQ 처리
- idempotency key handling
- reconnect flush
- conflict merge helper

## 검증 명령

```bash
make -C study/product-systems/01-offline-sync-foundations/problem test
make -C study/product-systems/01-offline-sync-foundations/problem app-build
make -C study/product-systems/01-offline-sync-foundations/problem app-test
```

## 읽는 순서

1. [problem/README.md](problem/README.md)
2. [react-native/README.md](react-native/README.md)
3. [docs/README.md](docs/README.md)
4. [notion/README.md](notion/README.md)

## 학습 포인트

- 제품 문제를 queue/retry 규칙 문제로 축소해 학습하기
- deterministic fake service로 offline 흐름을 검증하기
- 나중 프로젝트의 persistent outbox 설계를 위한 기반을 만들기

## 현재 상태

- 문제 정의: `verified`
- RN 구현: `verified`
- 개념 문서: `verified`
