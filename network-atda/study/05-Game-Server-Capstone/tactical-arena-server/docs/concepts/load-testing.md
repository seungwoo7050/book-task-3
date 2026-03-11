# Load Testing

## 목표

canonical smoke는 "여러 room에서 여러 bot이 동시에 로그인, 매치 시작, 종료, 결과 저장까지 끝나는가"를 확인하는 것이다.

## 현재 canonical smoke

- 명령: `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem load-test`
- 실제 검증 래퍼: `problem/script/load_smoke_test.py`
- 시나리오:
  - localhost server 기동
  - `arena_loadtest --room-count 2 --bots-per-room 4`
  - match 종료 후 SQLite 확인

## 확인 항목

- `arena_loadtest`가 `status=ok`로 종료한다.
- `match_history` row가 `2개 이상` 생성된다.
- `players` row가 `8개 이상` 생성된다.
- 서버가 timeout이나 crash 없이 smoke를 끝낸다.

## 구현 변경 메모

초기 버전의 `arena_loadtest`는 여러 스레드에서 `std::system("./arena_bot ...")`를 호출했다. 이 방식은 출력과 프로세스 제어가 불안정했고, 원래 계획한 "one-process bots"와도 어긋났다. 최종 버전은 in-process bot worker를 직접 구현해 load smoke를 안정화했다.

## 포트폴리오 설명 포인트

- authoritative server와 bot harness를 함께 제출할 수 있다.
- deterministic integration + smoke를 통해 "동작한다"를 코드와 리포트로 같이 설명할 수 있다.
- GUI 없이도 네트워크 서버 역량을 입증하는 형태다.
