# Structure Outline

## Chosen arc

1. 문제 범위를 먼저 MemTable contract로 좁힌다.
2. SkipList surface와 demo ordered output을 보여 준다.
3. level-0 ordering, tombstone, byte-size estimate, deterministic level generation을 invariant로 설명한다.
4. 마지막에는 go test 범위와 의도적으로 빠진 부분을 분리해 과장을 막는다.

## Why this structure

- 이 랩은 자료구조 구현이지만 저장 엔진 맥락이 더 중요해서, skip list 일반론보다 MemTable semantics를 앞세우는 편이 맞다.
- demo 출력이 tombstone과 ordered iteration을 함께 보여 줘서 본문 초반 증거로 쓰기 좋다.
- Go `internal/` 패키지 경계 때문에 즉석 외부 스니펫보다는 기존 테스트와 demo 중심 증거 구성이 더 안정적이다.

## Rejected alternatives

- skip list 알고리즘 일반론을 길게 풀어내는 구조는 버렸다.
- 메서드별 API 문서처럼 나열하는 구조도 버렸다.
- Python 버전과 1:1 대응 비교를 전면에 두는 구조는 버렸다. 이번 문서는 현재 Go 소스의 독립성을 먼저 보여 줘야 한다.
