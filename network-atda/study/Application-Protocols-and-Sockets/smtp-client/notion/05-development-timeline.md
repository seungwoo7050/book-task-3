# 05 개발 타임라인

        이 문서는 `SMTP Client`를 처음 재현하는 학생을 위한 가장 짧은 실행 순서를 정리한다. 핵심은 실제 메일 서비스를 붙이는 것이 아니라, 로컬 mock 서버에서 SMTP 대화를 단계별로 다시 확인하는 것이다.

        ## 준비
        - `python3`
        - `pytest`
        - 작업 위치: 저장소 루트 `/Users/woopinbell/work/book-task-3/network-atda`

        ## 단계 1. 문제와 제공물 확인
        먼저 아래 파일을 읽는다.
        - [`../problem/README.md`](../problem/README.md)
        - [`../problem/script/mock_smtp_server.py`](../problem/script/mock_smtp_server.py)
        - [`../problem/code/smtp_client_skeleton.py`](../problem/code/smtp_client_skeleton.py)

        여기서 확인할 질문:
        - 어떤 SMTP 명령 순서를 구현해야 하는가
        - 왜 외부 메일 서버가 아니라 mock 서버를 쓰는가
        - `DATA` 이후 종료 규칙은 무엇인가

        ## 단계 2. 구현과 테스트를 나란히 본다
        - [`../python/src/smtp_client.py`](../python/src/smtp_client.py)
        - [`../python/tests/test_smtp_client.py`](../python/tests/test_smtp_client.py)

        이 단계에서 볼 포인트:
        - greeting을 먼저 읽는가
        - `HELO`, `MAIL FROM`, `RCPT TO`, `DATA`, `QUIT`를 어떤 helper가 묶는가
        - 실패 응답을 즉시 멈추는가

        ## 단계 3. 자동 검증 먼저 실행
        아래 명령으로 mock 서버와 클라이언트를 함께 검증한다.

        ```bash
        make -C study/Application-Protocols-and-Sockets/smtp-client/problem test
        ```

        기대 결과:
        - 임시 mock SMTP 서버가 뜬다.
        - 클라이언트가 greeting부터 `QUIT`까지 정상 대화를 끝낸다.
        - greeting, `HELO`, 전체 세션 테스트가 통과한다.

        세부 테스트는 아래로 확인한다.

        ```bash
        cd study/Application-Protocols-and-Sockets/smtp-client/python/tests
        python3 -m pytest test_smtp_client.py -v
        ```

        ## 단계 4. 수동으로 SMTP 세션을 다시 본다
        터미널 1:

        ```bash
        python3 study/Application-Protocols-and-Sockets/smtp-client/problem/script/mock_smtp_server.py localhost 1025
        ```

        터미널 2:

        ```bash
        make -C study/Application-Protocols-and-Sockets/smtp-client/problem run-solution
        ```

        기대 결과:
        - 클라이언트가 오류 없이 종료된다.
        - 터미널 1의 mock 서버 로그에서 `HELO`, `MAIL FROM`, `RCPT TO`, `DATA`, `QUIT` 순서가 보인다.
        - `DATA` 본문 끝에는 `.` 한 줄이 들어가야 한다.

        ## 단계 5. 실패하면 가장 먼저 볼 곳
        - 세션이 초반부터 꼬이면 `220` greeting을 먼저 읽는지 확인한다.
        - `DATA` 후 응답이 안 오면 `
.
` 종료 규칙을 먼저 본다.
        - 서버가 명령을 못 읽으면 줄 끝이 `CRLF`인지 확인한다.
        - 관련 근거는 [`02-debug-log.md`](02-debug-log.md)에 정리했다.

        ## 단계 6. 완료 판정
        아래 조건을 만족하면 이 프로젝트는 재현한 것으로 본다.
        - 로컬 mock 서버가 왜 필요한지 설명할 수 있다.
        - `make test`가 통과한다.
        - 수동 실행에서 SMTP 명령 순서를 서버 로그로 확인했다.
        - envelope와 header의 차이를 설명할 수 있다.
