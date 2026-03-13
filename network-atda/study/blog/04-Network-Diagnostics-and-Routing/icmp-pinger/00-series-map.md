# ICMP Pinger 시리즈 지도

## 이 프로젝트를 한 줄로

시스템 ping을 흉내 내는 것이 아니라, ICMP Echo Request/Reply를 직접 조립하고 raw reply를 다시 뜯어 보며 진단 도구의 최소 형태를 만드는 기록이다.

## 시작 전에 고정한 자료

- 제공물: `problem/code/icmp_pinger_skeleton.py`, `problem/script/test_icmp.sh`
- 실행 진입점: `problem/Makefile`
- 사용자 답안: `study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/src/icmp_pinger.py`
- 보조 테스트: `study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/tests/test_icmp_pinger.py`

## 이 시리즈에서 따라갈 질문

1. checksum 계산과 packet build는 왜 하나의 규칙으로 같이 봐야 하는가.
2. raw socket으로 받은 reply에서 IPv4 header를 먼저 건너뛰어야 하는 이유는 무엇인가.
3. RTT 계산은 어떤 payload 형식에 기대고 있는가.
4. live raw-socket 실행과 fake-socket 테스트는 왜 반드시 분리해서 설명해야 하는가.

## 검증 명령

- deterministic test: `make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test`
- live run: `make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem run-solution HOST=google.com`
- live smoke: `sudo make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test-live HOST=google.com`

## 글 구성

| 파일 | 역할 |
| :--- | :--- |
| `00-series-map.md` | checksum, packet build, parsing, live 검증 경계를 먼저 잡는다. |
| `10-development-timeline.md` | packet 조립 → reply parsing → live 권한/통계 출력 순서로 이해를 쌓는다. |
