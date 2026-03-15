# Structure Outline

## Chosen arc

1. capstone 범위를 먼저 다시 제한해 reader가 운영 가능한 cluster를 기대하지 않게 만든다.
2. route -> leader append -> follower sync -> leader read surface를 첫 write 흐름으로 설명한다.
3. 그다음 disk replay, sequential offset, stale follower boundary를 invariant로 정리한다.
4. 마지막에 pytest와 수동 재실행 결과를 통해 "무엇이 통합됐고 무엇이 아직 빠졌는가"를 분리한다.

## Why this structure

- capstone은 구성 요소가 많아서 파일별 설명만 하면 쉽게 나열식 문서가 된다. 따라서 요청 흐름을 축으로 잡는 편이 더 읽기 좋다.
- 앞선 랩들과의 연결점을 살리려면 routing, replication, storage 세 요소가 어디서 맞물리는지 먼저 보여 줘야 한다.
- stale follower restart 관찰은 README만 읽어서는 놓치기 쉬운 중요한 경계라서 invariant 장에 반드시 포함시켰다.

## Rejected alternatives

- 기능 목록 중심 설명은 버렸다. 이 capstone의 가치는 기능 수보다 경로 통합에 있다.
- FastAPI 엔드포인트 문서처럼 쓰는 구조도 버렸다. 외부 API보다 내부 orchestration이 더 중요하다.
- "분산 KV 완성" 서사는 source-first 원칙을 해쳐서 제외했다.
