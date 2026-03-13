# ICMP Pinger — Development Timeline

ICMP Pinger를 다시 쓸 때 가장 먼저 고정한 건 `make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test`가 기대하는 실행 표면이었다. 기존 blog 초안은 `_legacy/2026-03-13-isolate-and-rewrite/04-Network-Diagnostics-and-Routing/icmp-pinger`로 옮기고, 이번 글은 `README.md`, `problem/Makefile`, 그리고 `python/src/`와 `python/tests/`만으로 chronology를 복원했다.

```bash
make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test
sudo make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test-live HOST=google.com
```

## Session 1 — 실행 entrypoint와 최소 runtime surface를 먼저 고정했다
먼저 붙든 질문은 "README보다 먼저 실제 entrypoint가 어떤 입력과 출력 surface를 갖는지 잡아야 한다"였다. 그래서 작업 단위도 `python/src/icmp_pinger.py::ping`처럼 작게 잘랐다. 실제 조치는 핵심 entrypoint인 `python/src/icmp_pinger.py::ping`를 기준으로 socket/event loop 또는 main flow를 먼저 닫았다.
이 구간의 기준 명령은 `make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test`였고, 여기서 확인한 신호는 다음과 같았다. run surface가 정리되면서 이후 판단을 함수 단위로 이어 붙일 수 있게 된 상태. 이 단계가 남긴 개념 메모도 분명했다. RFC 1071 인터넷 체크섬.

## Session 2 — 핵심 protocol/algorithm branch를 채웠다
먼저 붙든 질문은 "이 프로젝트의 핵심은 설명문이 아니라 request/reply, timer, cache, parser 같은 작은 branch에 숨어 있다"였다. 그래서 작업 단위도 `python/src/icmp_pinger.py::parse_echo_reply`처럼 작게 잘랐다. 실제 조치는 `python/src/icmp_pinger.py::parse_echo_reply`를 중심으로 프로젝트 고유 규칙을 구현하고, 성공/실패 branch가 어디서 갈리는지 드러냈다.
이 구간의 기준 명령은 `make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test`였고, 여기서 확인한 신호는 다음과 같았다. 핵심 로직이 눈에 보이는 함수 단위로 정리되면서 test가 기대하는 입출력과 연결된 상태. 이 단계가 남긴 개념 메모도 분명했다. raw socket 권한 모델.

## Session 3 — canonical test와 문서로 경계를 닫았다
먼저 붙든 질문은 "좋은 chronology는 마지막에 test result와 남은 한계를 같이 남겨야 과장되지 않는다"였다. 그래서 작업 단위도 `python/tests/test_icmp_pinger.py`처럼 작게 잘랐다. 실제 조치는 canonical test를 다시 돌리고, docs/concepts와 현재 한계를 함께 묶어 마감했다.
이 구간의 기준 명령은 `sudo make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test-live HOST=google.com`였고, 여기서 확인한 신호는 다음과 같았다. pytest: `./python/tests` 11 passed; live raw-socket check는 sudo 별도. 이 단계가 남긴 개념 메모도 분명했다. RFC 1071 인터넷 체크섬와 raw socket 권한 모델.

## Verification and Boundaries
이번 rewrite에서도 `make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test`를 다시 실행해 pytest: `./python/tests` 11 passed; live raw-socket check는 sudo 별도 결과를 확인했다. 글은 결과 자랑으로 끝내지 않고, 지금 남아 있는 범위를 아래처럼 고정한다.
- IPv6/ICMPv6는 지원하지 않습니다.
- 시스템 `ping` 수준의 상세 통계는 제공하지 않습니다.
- live raw-socket 실행은 OS와 방화벽 정책에 영향을 받습니다.
