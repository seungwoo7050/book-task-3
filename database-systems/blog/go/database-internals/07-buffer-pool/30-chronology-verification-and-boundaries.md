# Verification And Boundaries

## 1. 자동 검증은 fetch, cache reuse, dirty, eviction을 넓게 덮는다

2026-03-14 기준 재실행 명령은 아래와 같다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/07-buffer-pool
GOWORK=off go test ./...
```

결과는 아래처럼 통과했다.

```text
ok  	study.local/go/database-internals/projects/07-buffer-pool/tests	(cached)
```

테스트가 잡는 항목은 다음과 같다.

- disk fetch
- cached page instance reuse
- dirty flag tracking
- unpinned page eviction
- LRU cache 기본 동작

즉 buffer pool 자체와 replacer 기본 동작을 함께 확인한다.

## 2. demo와 추가 재실행 관찰값

demo 출력:

```text
page-1
```

추가 재실행 출력:

```text
disk_after_flush modified
pinned_evict_error true
```

이 결과를 합치면 현재 구현은 아래 사실을 만족한다.

- page id parsing으로 정확한 disk page를 읽는다
- dirty page는 flush 뒤 실제 file bytes를 바꾼다
- pinned page는 eviction 대상이 되지 못하고 현재 구현은 에러를 반환한다

## 3. 현재 구현이 일부러 다루지 않는 것

이 랩을 full DB buffer manager로 읽으면 안 된다.

- concurrent latch가 없다
- lock manager와 transaction coordination이 없다
- async prefetch/flush가 없다
- free frame search를 반복하는 smarter replacer가 없다
- page allocation이나 file growth management가 없다

즉 현재 focus는 single-process page lifecycle semantics를 고정하는 데 있다.

## 4. 이 문서에서 피한 과장

이번 재작성에서는 아래 같은 표현을 쓰지 않았다.

- "실전 DBMS buffer pool을 완성했다"
- "eviction 전략을 충분히 최적화했다"
- "concurrent workload도 안전하게 처리한다"

현재 소스와 테스트가 실제로 보여 주는 것은 pin count, dirty flush, LRU-based candidate selection, pinned eviction error까지다. 그보다 큰 시스템 claim은 근거가 없다.
