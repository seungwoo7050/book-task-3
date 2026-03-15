# Structure Outline

## Chosen arc

1. 문제 범위를 immutable file format으로 좁힌다.
2. demo 출력으로 reopen 뒤 lookup surface를 먼저 보여 준다.
3. sorted input, footer layout, tombstone sentinel, 2-step lookup read를 invariant로 정리한다.
4. 마지막에 malformed footer와 현재 비워 둔 storage concerns를 분리해 적는다.

## Why this structure

- 이 랩은 binary layout이 핵심이라 section 단위 설명이 자연스럽다.
- shared serializer까지 짧게 연결해야 tombstone sentinel 설명이 소스 근거를 갖는다.
- demo가 value, tombstone, missing을 모두 보여 줘서 초반 evidence로 쓰기 좋다.

## Rejected alternatives

- SSTable 일반론을 길게 설명하는 구조는 버렸다.
- 테스트 목록만 나열하는 구조도 버렸다.
- compaction까지 미리 끌어오는 서술은 현재 소스 범위를 벗어나서 제외했다.
