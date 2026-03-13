# 30 Smoke Verification And Boundaries

## 2026-03-11
### Session 1

- 목표: 현재 공개 표면이 정말 `verified` 상태를 설명하는지 확인한다.
- 진행: `Makefile`, `cpp/README.md`, `tests/test_eventlab.py`를 함께 읽어 canonical rerun path와 pass signal을 고정했다.
- 판단: `eventlab`의 검증은 단위 함수 호출이 아니라 실제 프로세스를 띄우고 두 client로 welcome, echo, ping/pong, idle keep-alive, quit를 모두 관찰하는 smoke path에 있다.
- 검증: README 표면은 `verified`, 테스트 파일의 최종 신호는 `eventlab smoke passed.`다.
- 다음: parser 책임은 다음 lab인 `msglab`에서 별도 transcript로 분리한다.

CLI:

```bash
$ cd study/shared-core/01-eventlab/cpp
$ sed -n '1,200p' Makefile
$ sed -n '1,220p' tests/test_eventlab.py
$ make clean && make test
```

출력:

```text
eventlab smoke passed.
```

이 시점의 핵심 코드는 테스트 쪽에 있었다.

```python
send_line(a, "PING keepalive")
pong = recv_text(a, time.time() + 3, "PONG keepalive")

idle_ping = recv_text(b, time.time() + 5, "PING :idle-check")
if "PING :idle-check" not in idle_ping:
    raise RuntimeError("idle keep-alive ping did not arrive")
```

나중에 보니 이 검증은 단순히 명령 두 개를 확인하는 수준이 아니었다. 한 연결은 적극적으로 `PING`을 보내고 다른 연결은 일부러 idle로 두면서, read/write loop와 keep-alive cutoff가 같은 runtime에서 함께 굴러가는지를 한 번에 묶어 확인한다.

현재 경계:

- 포함: accept, newline framing, `ECHO`, `PING`/`PONG`, `QUIT`, idle keep-alive
- 제외: structured parser, registration, room state, game rule

