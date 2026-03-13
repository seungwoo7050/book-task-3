    # Structure Design — SMTP Client

    ## opening
    - 시작 질문: 이 프로젝트를 실제로 어디서부터 만들기 시작했는가.
    - 바로 보여 줄 증거: `make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem test`와 ``python/src/smtp_client.py::main``.
    - 서술 원칙: 결과 요약보다 Session별 판단 이동을 우선한다.
    - 메모: `make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem test`가 통과하는 상태를 출발점으로 삼되, 실제 글의 첫 장면은 ``python/src/smtp_client.py::main``에서 시작한다.

    ## Session 1 — 실행 entrypoint와 최소 runtime surface를 먼저 고정했다
- 다룰 파일/표면: `python/src/smtp_client.py::main`
- 글에서 먼저 던질 질문: "README보다 먼저 실제 entrypoint가 어떤 입력과 출력 surface를 갖는지 잡아야 한다"
- 꼭 넣을 CLI: `make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem run-solution`
- 꼭 남길 검증 신호: run surface가 정리되면서 이후 판단을 함수 단위로 이어 붙일 수 있게 됐다.
- 핵심 전환 문장: 3자리 SMTP 응답 코드에 따른 제어 흐름
## Session 2 — 핵심 protocol/algorithm branch를 채웠다
- 다룰 파일/표면: `python/src/smtp_client.py::send_command`
- 글에서 먼저 던질 질문: "이 프로젝트의 핵심은 설명문이 아니라 request/reply, timer, cache, parser 같은 작은 branch에 숨어 있다"
- 꼭 넣을 CLI: `make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem run-solution`
- 꼭 남길 검증 신호: 핵심 로직이 눈에 보이는 함수 단위로 정리되면서 test가 기대하는 입출력과 연결됐다.
- 핵심 전환 문장: `CRLF`와 `DATA` 종료 구분자 처리
## Session 3 — canonical test와 문서로 경계를 닫았다
- 다룰 파일/표면: `python/tests/test_smtp_client.py`, `make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem test`, `docs/concepts/email-format.md`
- 글에서 먼저 던질 질문: "좋은 chronology는 마지막에 test result와 남은 한계를 같이 남겨야 과장되지 않는다"
- 꼭 넣을 CLI: `make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem test`
- 꼭 남길 검증 신호: SMTP Client Test Suite: 전체 SMTP dialogue 완료, 성공 메시지와 대화 로그 확인, 총 3 passed
- 핵심 전환 문장: 3자리 SMTP 응답 코드에 따른 제어 흐름 and `CRLF`와 `DATA` 종료 구분자 처리

    ## ending
    - 마지막 단락에서는 현재 한계를 README bullet 그대로 축약해 남긴다.
    - `STARTTLS`는 구현하지 않았습니다.
- `AUTH LOGIN`은 구현하지 않았습니다.
- 외부 SMTP 서버 정책과의 차이는 검증하지 않았습니다.
