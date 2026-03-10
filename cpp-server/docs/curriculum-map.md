# 커리큘럼 맵

## 왜 이런 모양으로 재구성했는가

이 저장소는 예전의 큰 C++ 서버 작업을 그대로 보여 주지 않는다. 대신 한 번에 너무 많은 층이 섞여 있던 문제를, 학습자가 단계별로 따라갈 수 있는 6개의 lab으로 다시 나눴다. 기준은 단순하다.

1. 각 lab은 독립적으로 읽히고 독립적으로 검증되어야 한다.
2. IRC 서버와 게임 서버는 같은 저장소 안에 있어도 학습 질문이 섞이지 않아야 한다.
3. 마지막 capstone은 곧바로 공개 포트폴리오로 확장 가능한 형태여야 한다.

## lab 순서

1. `eventlab`
   - 질문: 서버는 연결을 받고 읽고 쓰고 정리하는 최소 단위에서 어떻게 움직이는가
   - 결과물: non-blocking TCP loop, keep-alive, smoke test
2. `msglab`
   - 질문: parser와 validator는 네트워크 I/O와 어떻게 분리해야 하는가
   - 결과물: `Message`, `Parser`, transcript 기반 테스트
3. `roomlab`
   - 질문: IRC subset 서버에서 등록과 room lifecycle은 어떤 상태 전이로 보이는가
   - 결과물: registration, JOIN/PART, broadcast, disconnect cleanup
4. `ticklab`
   - 질문: authoritative simulation은 transport 없이도 검증 가능한가
   - 결과물: fixed-step engine, reconnect grace, deterministic test
5. `ircserv`
   - 질문: 앞선 IRC lab을 합쳐 capstone으로 만들면 무엇이 추가되어야 하는가
   - 결과물: modern IRC command surface, channel privilege, smoke test
6. `arenaserv`
   - 질문: authoritative game server에서 세션 연속성과 room state machine을 최소 범위로 어떻게 보여 줄 수 있는가
   - 결과물: pure TCP arena server, snapshot broadcast, reconnect, multi-client smoke test

## 왜 이 순서가 학습에 유리한가

- `eventlab`은 커널 이벤트와 연결 수명주기를 먼저 고립시킨다.
- `msglab`은 parser를 네트워크와 분리해, 나중에 버그가 생겼을 때 어느 층을 봐야 하는지 명확하게 만든다.
- `roomlab`은 실제 서버 상태 전이와 IRC subset을 묶어 본다.
- `ticklab`은 게임 서버에서 중요한 authoritative 판단을 transport보다 먼저 검증하게 한다.
- `ircserv`는 IRC 축의 capstone으로, protocol completeness를 보여 주는 자리다.
- `arenaserv`는 게임 서버 축의 capstone으로, state continuity와 reconnect를 보여 주는 자리다.

## 학생이 이 레포에서 가져가면 좋은 것

- “작은 질문을 먼저 분리해 검증한 다음 capstone으로 합친다”는 커리큘럼 설계법
- README, 개념 노트, 학습 노트, 테스트 증거를 분리하는 문서 구조
- 포트폴리오 레포에서 어떤 지점을 데모 영상, 로그, 설계 설명으로 보여 주면 좋은지에 대한 힌트

## 의도적으로 뺀 것

- WebSocket과 브라우저 클라이언트
- 운영 배포 구성(Nginx, Docker Compose, DB, metrics)
- 게임 규칙 전체를 제품 수준으로 확장하는 작업

이 요소들은 흥미롭지만, 현재 커리큘럼의 핵심 질문을 흐리기 때문에 공식 학습 범위에서는 제외한다.
