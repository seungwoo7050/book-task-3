# eventlab 3. smoke test가 실제로 증명하는 범위

`eventlab`의 검증은 화려하지 않다. 하지만 [`cpp/tests/test_eventlab.py`](../../../shared-core/01-eventlab/cpp/tests/test_eventlab.py) 한 파일이 잡는 장면은 생각보다 넓다. 테스트는 서버를 subprocess로 띄우고, 포트가 열릴 때까지 기다린 뒤, 두 개의 raw TCP 클라이언트를 붙인다. 그리고 그 위에서 서버가 최소 runtime으로서 무엇까지 버티는지를 차례대로 본다.

검증 흐름은 비교적 단순하다. 두 연결이 모두 `WELCOME`을 받는지 확인하고, 첫 번째 클라이언트가 일반 텍스트를 보내면 `ECHO ...`가 돌아오는지 본다. 이어서 `PING keepalive`에 `PONG keepalive`가 오는지 확인한 뒤, 두 번째 클라이언트는 일부러 idle 상태로 두어 `PING :idle-check`가 도착하는지 기다린다. 마지막으로 `QUIT`에 `BYE`가 오는지 확인하고 프로세스를 정리한다.

```py
send_line(a, "PING keepalive")
pong = recv_text(a, time.time() + 3, "PONG keepalive")

time.sleep(3)
idle_ping = recv_text(b, time.time() + 5, "PING :idle-check")
```

직접 실행한 CLI도 같은 장면으로 닫힌다.

```sh
cd /Users/woopinbell/work/book-task-3/cpp-server/study/shared-core/01-eventlab/cpp
make clean && make test
```

```text
python3 tests/test_eventlab.py
eventlab smoke passed.
```

이 결과가 뜻하는 바는 분명하다. 현재 구현은 accept/read/write loop, line protocol, idle keep-alive, graceful quit까지는 실제 소켓 표면에서 확인된다. 특히 두 번째 클라이언트를 일부러 가만히 두고 idle ping을 기다리는 장면 덕분에, keep-alive가 코드에만 있는 것이 아니라 네트워크 표면까지 도달했다는 것도 확인된다.

동시에 이 테스트가 아직 증명하지 않는 것도 선명하다. parser는 아직 구조화되지 않았고, 상태 전이는 없다. partial write 재시도나 backpressure도 깊게 다루지 않는다. `eventlab`이 여기서 멈추는 이유가 바로 그것이다. 런타임의 바닥을 먼저 고정했으니, 다음 문서인 [`../02-msglab/README.md`](../02-msglab/README.md)부터는 그 위에 올라갈 parser 경계를 따로 떼어 읽을 수 있다.

