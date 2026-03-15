# Structure Outline

## Core thesis

이 capstone의 가치는 "분산 KV를 완성했다"가 아니라, routing, append-only persistence, follower catch-up, restart replay를 한 요청 경로로 묶어 보여 준다는 데 있다.

## Writing plan

1. problem 문서로 범위를 먼저 줄인다.
2. `NewCluster`와 `RouteShard`로 정적 topology와 write target 선택을 설명한다.
3. `Store.Apply`와 `SyncFollower`로 append/replication invariant를 설명한다.
4. `RestartNode`와 임시 boundary check로 recovery 범위를 좁혀 적는다.
5. test, demo, on-disk log를 함께 보여 주며 검증과 한계를 마무리한다.

## Must-keep evidence

- `NewCluster`의 static replica group construction
- `Store.Apply`의 sequential offset rule
- `SyncFollower`의 `Watermark()+1`
- demo output과 `.demo-data` log files
- `restart_without_sync_ok=false`
