# 02 디버그 로그

이 파일은 과거의 날짜 순서를 복원하려는 문서가 아니다. 백업 노트와 현재 테스트를 함께 보고, 지금도 재현하거나 설명할 수 있는 문제만 남긴다.

## 사례 1. TCP 로그인은 성공했는데 UDP 입력이 매치에 연결되지 않음
- 증상: 클라이언트가 `MATCH_START`를 받았는데도 입력이 적용되지 않았다.
- 원인: TCP 세션과 UDP endpoint를 같은 플레이어/매치 상태에 정확히 묶는 handoff가 필요했다.
- 수정: `UDP_BIND`/heartbeat와 match/player 식별 정보를 사용해 UDP endpoint 등록 단계를 명시적으로 뒀다.
- 확인: bot demo와 integration 시나리오에서 입력 반영 여부로 확인했다.

## 사례 2. 재접속 후 다른 세션처럼 취급되어 매치 상태가 끊김
- 증상: TCP 재연결은 됐지만 기존 플레이어 상태를 이어받지 못하고 새 세션처럼 동작했다.
- 원인: reconnect는 소켓 재연결만으로 끝나지 않고 player id, token, match 상태를 함께 복원해야 한다.
- 수정: `RESUME token=...` 흐름과 `resume_window_ms` 정책을 두고 기존 상태를 복구하도록 구현했다.
- 확인: `scenario_resume_same_player` integration test로 확인했다.

## 사례 3. out-of-order UDP 입력이 시뮬레이션을 되돌리거나 왜곡함
- 증상: 늦게 도착한 입력이 이미 처리한 틱을 덮어쓰는 문제가 생길 수 있었다.
- 원인: UDP는 순서를 보장하지 않으므로 sequence 기준으로 오래된 입력을 구분해야 한다.
- 수정: input packet에 sequence를 넣고, 매치 상태에서 더 오래된 입력은 무시하도록 정리했다.
- 확인: `scenario_out_of_order_udp` integration test로 검증했다.

## 사례 4. 매치 종료 후 DB 전적이 부분 업데이트될 위험
- 증상: 승패와 킬/데스가 한쪽만 저장되면 다음 로그인 프로필이 어긋날 수 있었다.
- 원인: 결과 저장이 여러 SQL 문으로 흩어지면 중간 실패 시 일관성이 깨진다.
- 수정: `record_match()`를 트랜잭션으로 묶어 match history와 player stats를 함께 갱신했다.
- 확인: `test_repository.cpp`와 demo DB 확인 로그로 검증했다.
