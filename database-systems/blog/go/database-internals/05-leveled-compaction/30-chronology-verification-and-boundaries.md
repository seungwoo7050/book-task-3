# Verification And Boundaries

## 1. 자동 검증은 merge semantics와 metadata 경로를 함께 덮는다

2026-03-14 기준 재실행 명령은 아래와 같다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/05-leveled-compaction
GOWORK=off go test ./...
```

결과는 아래처럼 통과했다.

```text
ok  	study.local/go/database-internals/projects/05-leveled-compaction/tests	(cached)
```

테스트가 잡는 항목은 다음과 같다.

- newer value precedence
- deepest-level tombstone drop
- L0->L1 compaction 결과 파일/삭제 파일/lookup
- removed input file cleanup
- manifest round trip

즉 현재 범위 안에서는 merge correctness와 metadata persistence가 모두 검증된다.

## 2. demo와 추가 재실행 관찰값

demo 출력:

```text
apple=red
banana=gold
pear=green
```

추가 재실행 출력:

```text
drop_at_deepest true 000003.sst [000003.sst]
lookup_after_drop false true
keep_above_deepest false 000003.sst
lookup_after_keep true true
```

이 값들을 합치면 현재 구현은 아래 사실을 만족한다.

- newer file의 overwrite가 old value를 가린다
- deepest compaction에서는 tombstone이 실제로 제거될 수 있다
- 더 깊은 level이 남아 있으면 tombstone은 유지된다

## 3. 현재 구현이 일부러 다루지 않는 것

이 랩을 production compaction scheduler로 읽으면 안 된다.

- background scheduling이 없다
- size policy와 score-based selection이 없다
- L1 이상의 일반화된 multi-level balancing이 없다
- concurrent readers/writers coordination이 없다
- manifest journaling이나 failure rollback이 없다

즉 compaction 자체보다, compaction 한 번을 semantic-safe하게 수행하는 최소 경로에 집중한다.

## 4. 이 문서에서 피한 과장

이번 재작성에서는 아래 같은 표현을 쓰지 않았다.

- "leveled compaction 시스템을 완성했다"
- "manifest crash safety를 포괄적으로 해결했다"
- "production compaction scheduler를 구현했다"

현재 소스와 테스트가 실제로 보여 주는 것은 newest-first merge, conditional tombstone drop, atomic manifest file write, old input cleanup까지다. 그보다 큰 운영 claim은 근거가 없다.
