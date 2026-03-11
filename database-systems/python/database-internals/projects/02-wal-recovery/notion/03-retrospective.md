# 회고

## 이번 단계에서 명확해진 것
- durability는 “무엇을 먼저 쓰는가”의 문제이며, append-ahead 규칙 하나로 많은 설명이 정리됩니다.
- replay policy는 완벽한 복구보다 “어디까지 믿을 것인가”를 명확히 하는 쪽이 더 중요합니다.
- flush 이후 WAL rotation까지 마쳐야 읽기 경로와 복구 경계가 깔끔해집니다.

## 아직 단순화한 부분
- fsync 빈도, segment rolling, background checkpoint 같은 운영 이슈는 빠져 있습니다.
- single-process 전제라 concurrent writer나 replication replay는 다루지 않습니다.

## 다음에 확장한다면
- segment 단위 WAL과 checkpoint를 넣어 recovery 시간을 줄일 수 있습니다.
- flush 전후 failure injection을 넣어 durability 경계를 더 엄밀하게 검증할 수 있습니다.

## `03 Index Filter`로 넘길 질문
- 겹치는 SSTable이 계속 쌓일 때 WAL과 별개로 어떤 정리(compaction)가 필요한가?
- point lookup 비용을 줄이려면 index와 filter를 어디에 붙여야 하는가?
