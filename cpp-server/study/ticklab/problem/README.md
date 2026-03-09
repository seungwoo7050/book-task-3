# ticklab Problem

이 문서는 원본 과제 문서가 없는 상태에서 `legacy/` 코드를 바탕으로 재구성한 문제 설명이다.

## Reconstructed Prompt

C++17로 authoritative fixed-step simulation engine을 작성한다. 엔진은 다음을 지원해야 한다.

- room queue와 ready 기반 countdown
- monotonic input sequence 검증
- fixed tick마다 state advance와 snapshot 생성
- projectile hit, elimination, round timeout draw
- reconnect grace window와 snapshot 재전송

## Deliverables

- headless C++17 match engine
- deterministic transcript fixture 기반 unit tests

## Provenance

| source | why it matters |
| --- | --- |
| `legacy/src/GameRoom.cpp` | room ownership과 match lifecycle 아이디어의 참고 자료 |
| `legacy/src/GameLogic.cpp` | authoritative 판정이 서버에 있어야 한다는 근거 |
| `legacy/docs/game-protocol.md` | 이벤트 스트림을 명령/이벤트로 분리해 적는 방식의 참고 자료 |
| `legacy/docs/portfolio-checklist.md` | game server 시연에서 필요한 최소 이벤트 증거의 참고 자료 |
