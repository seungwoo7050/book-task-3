# Web Server 개발 타임라인

## Day 1

### Session 1

- 목표: skeleton을 열기 전에, 이 과제가 무엇을 하라는 건지부터 `problem/README.md`와 `Makefile`로 고정한다.
- 진행: `run-server`, `run-solution`, `test`, `request` — Makefile 타깃 네 개가 보였다. `test` 안을 보니 solution을 background로 띄우고 `test_server.sh`를 돌리는 구조였다. skeleton은 `code/server_skeleton.py`에, 샘플 HTML은 `data/hello.html`에 있었다.
- 이슈: 이 시점에서 가장 헷갈렸던 건 "어디서 서버를 실행해야 하는가"였다. Makefile의 `cd $(DATA_DIR)` 때문에 서버가 `data/` 안에서 뜬다는 사실을 놓치면, 파일 경로가 영뚱하게 풀렸다.
- 판단: 구현을 건드리기 전에 `make run-solution → make request → make test` 순서로 한 번 돌려 봐야 했다.

CLI:

```bash
$ make -C study/01-Application-Protocols-and-Sockets/web-server/problem run-solution
[INFO] Web server started on port 6789
[INFO] Serving files from: .../problem/data
```

```bash
$ make -C study/01-Application-Protocols-and-Sockets/web-server/problem request
*   Trying 127.0.0.1:6789...
* Connected to localhost (127.0.0.1) port 6789
> GET /hello.html HTTP/1.1
< HTTP/1.1 200 OK
< Content-Type: text/html
< Content-Length: 184
< Connection: close
```

첫 `curl -v` 결과에서 `200 OK`와 `Connection: close`가 보였다. 이때까지는 그냥 "동작한다"로 끝날 뻔했는데, `make test`를 따로 돌려야 한다는 점을 놓칠 수 없었다.

### Session 2

- 목표: skeleton을 열어서 실제로 채워야 할 부분이 무엇인지 윤곽을 잡는다.
- 진행: `server_skeleton.py`에는 socket 생성과 accept loop까지만 있었다. 요청 파싱, 파일 읽기, 응답 조립, 404 처리, thread 분리가 전부 비어 있었다.
- 이슈: 당시 의문은 "요청을 통째로 `recv`하면 되나, 아니면 줄 단위로 읽어야 하나"였다. 교과서적으로는 `\r\n\r\n`까지 읽어야 하지만, 이 과제의 테스트는 4KB 한 번 `recv`로 충분했다.

요청 라인 파싱은 이렇게 시작했다.

```py
request_line = message.splitlines()[0]
tokens = request_line.split()
filename = tokens[1][1:]
```

당시에는 이게 어떤 의미인지 잘 안 읽혔다. `tokens[1]`이 `/hello.html`이니 앞의 `/`을 잘라서 상대 경로로 바꾸는 건데, 이 한 줄이 서버의 루트 디렉터리 바깥으로 나갈 수 있다는 뜻이기도 했다. path traversal 방어는 이 과제 범위 밖이어서 넘어갔지만, 처음으로 "서버 코드에서 경로를 그대로 믿으면 안 된다"는 감각이 생겼다.

### Session 3

- 목표: `/`가 요청으로 들어왔을 때 어떻게 처리할지 결정한다.
- 이슈: `tokens[1]`이 `/`이면 `filename`이 빈 문자열이 된다. 이걸 그냥 두면 `open("")`이 되고, OS마다 다른 에러가 난다.
- 판단: 이 과제의 `data/` 폴더에는 `hello.html` 하나뿐이니 빈 경로를 `hello.html`로 치환하기로 했다.

```py
if filename == "":
    filename = "hello.html"
```

이때까지는 이 분기가 과제용 편의 처리라고만 생각했는데, 나중에 `make test`를 돌려 보니 검증 스크립트가 `/` 요청과 `/hello.html` 요청 둘 다 보내고 있었다. 즉 이 분기가 없으면 테스트가 반만 통과한다.

### Session 4

- 목표: 200 응답과 404 응답의 계약을 완성한다.
- 진행: 파일 읽기가 성공하면 `Content-Type`, `Content-Length`, `Connection: close`를 채운 헤더를 조립했다 .

```py
header = (
    f"HTTP/1.1 200 OK\r\n"
    f"Content-Type: {content_type}\r\n"
    f"Content-Length: {len(body)}\r\n"
    f"Connection: close\r\n"
    f"\r\n"
)
connection_socket.sendall(header.encode() + body)
```

- 이슈: 처음에 `Content-Length`를 빼고 본문만 보내 봤더니 `curl`은 잘 받았다. 하지만 `test_server.sh`는 `Content-Length` 헤더가 있는지 검사하고 있었다. `curl`만으로 "됐다"고 말할 수 없었던 이유가 여기 있었다.
- 조치: `FileNotFoundError`를 잡아서 404 응답을 보내는 분기를 추가했다. 404 응답도 `Content-Length`를 갖춰야 했다.

```bash
$ curl -i http://localhost:6789/missing.html
HTTP/1.1 404 Not Found
Content-Type: text/html
Content-Length: 127
Connection: close
```

### Session 5

- 목표: thread-per-connection 구조를 넣고 전체를 묶는다.
- 진행: `server_socket.accept()` 후 `threading.Thread(target=handle_client, ...)`를 만들고 `daemon=True`로 설정했다.
- 이슈: daemon thread를 쓰지 않으면 서버를 Ctrl+C로 죽여도 남아 있는 thread 때문에 프로세스가 안 끝났다. 당시에는 "왜 안 죽지?" 하고 한참 기다렸는데, daemon 설정 한 줄이 답이었다.
- 검증: `make test` 최종 실행.

CLI:

```bash
$ make -C study/01-Application-Protocols-and-Sockets/web-server/problem test
Testing Web Server on localhost:6789...
✓ GET /hello.html returns 200 OK
✓ GET / returns 200 OK
✓ GET /missing.html returns 404 Not Found
✓ Response includes Content-Length header
✓ Response includes Connection: close
All tests passed!
```

- 정리:
  - 이 프로젝트의 핵심은 `handle_client()` 안의 파싱 → 읽기 → 응답 조립 흐름이었다.
  - 처음 가설은 "socket만 열면 서버"였지만, 실제로는 HTTP 응답 계약(헤더 규격, Content-Length, Connection: close)이 서버의 정체성이었다.
  - `curl` 한 번 성공으로 안심하면 안 되고, 자동화된 검증 스크립트가 여러 시나리오를 함께 돌려야 한다는 점도 분명해졌다.
  - 다음은 UDP socket으로 넘어간다. TCP의 연결 기반 구조가 사라지면 클라이언트가 어떤 책임을 추가로 져야 하는지 볼 차례다.
