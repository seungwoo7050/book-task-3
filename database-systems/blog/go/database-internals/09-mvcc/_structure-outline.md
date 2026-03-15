# Structure Outline

## Chosen arc

1. full transaction engine가 아니라 snapshot isolation의 최소 규칙이라는 범위를 먼저 잡는다.
2. demo와 추가 재실행으로 snapshot read, conflict, GC 결과를 먼저 보여 준다.
3. snapshot watermark, read-your-own-write, commit-time conflict, GC trimming을 invariant로 정리한다.
4. 마지막에는 phantom control과 distributed transaction이 아직 없다는 점을 분리한다.

## Why this structure

- 이 랩은 버전 체인과 트랜잭션 메타데이터가 같이 움직여서, 두 축을 같이 설명하는 편이 읽기 쉽다.
- conflict abort와 GC trimming은 테스트로도 보이지만 추가 관찰값으로 묶으면 훨씬 선명해진다.
- source-only nuance인 "old versions 중 하나는 남긴다"를 GC 설명에 명시하는 편이 좋다.

## Rejected alternatives

- 격리 수준 일반론을 길게 푸는 구조는 버렸다.
- MVCC를 SQL 엔진 서사로 확대하는 구조도 버렸다.
- lock manager까지 상상으로 연결하는 서사는 현재 범위를 벗어나 제외했다.
