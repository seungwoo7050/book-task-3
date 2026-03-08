# Study 3 Capstone

이 capstone은 한국어 회의 지원 시스템을 제출 가능한 데모로 마감하는 프로젝트다.

## Core Promise

- 회의를 chunked STT 기준으로 near-realtime 캡처한다.
- 토픽 전환과 쟁점을 구조화한다.
- 개입 시점에 summary/question/decision-option/next-action을 제시한다.
- 필요한 자료를 수집하고 replayable demo로 검증한다.

## Version Rule

1. `v0-initial-demo`: chunked STT, topic shift detection, issue cards, timeline
2. `v1-live-intervention`: intervention timing engine, action generation, 자료 수집/요약
3. `v2-submission-polish`: issue relation graph, replayable demo, 제출 마감

버전은 항상 이전 폴더를 복제한 뒤 수정한다.
