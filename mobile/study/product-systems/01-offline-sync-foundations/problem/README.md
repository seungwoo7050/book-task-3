# Problem: Offline Sync Foundations

> Status: VERIFIED
> Scope: queue / retry / replay foundation
> Last Checked: 2026-03-12

## 문제 요약

deterministic fake sync service를 사용해 outbox, retry, DLQ, idempotency, pull-after-push merge 규칙을 검증한다.

## 왜 이 문제가 커리큘럼에 필요한가

local-first 제품 과제를 바로 풀기 전에 sync 규칙만 독립 변수로 다루기 위해 만든 브리지 문제다.
이 과제의 목적은 채팅 앱이나 캡스톤에서 반복될 queue/retry 패턴을 먼저 몸에 익히는 것이다.

## 제공 자료

- 새로 설계한 offline-sync foundations 문제 정의
- `problem/code/README.md`의 sync scaffold
- `problem/script/README.md`의 보조 스크립트 안내
- `problem/data/README.md`의 fixture 설명

## 필수 요구사항

1. task create queue
2. retry and DLQ
3. idempotency key handling
4. reconnect flush
5. conflict merge helper

## 의도적 비범위

- 실제 원격 서버 연동
- persistent database 계층
- push notification 기반 sync trigger

## 평가/검증 기준

```bash
make test
make app-build
make app-test
```

- queue와 retry 규칙이 deterministic해야 한다.
- conflict merge helper가 재현 가능한 결과를 내야 한다.
- RN 앱 검증이 같은 모델을 공유해야 한다.

## 원문/출처 보존 위치

- [SOURCE-PROVENANCE.md](SOURCE-PROVENANCE.md)
- [code/README.md](code/README.md)
- [script/README.md](script/README.md)
- [data/README.md](data/README.md)
