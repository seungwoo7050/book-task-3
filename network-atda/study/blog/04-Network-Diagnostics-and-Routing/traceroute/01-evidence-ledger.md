# Traceroute Evidence Ledger

## 이번에 읽은 자료

- 문제 사양: `study/04-Network-Diagnostics-and-Routing/traceroute/problem/README.md`
- 구현 엔트리: `study/04-Network-Diagnostics-and-Routing/traceroute/python/src/traceroute.py`
- 보조 테스트: `study/04-Network-Diagnostics-and-Routing/traceroute/python/tests/test_traceroute.py`
- 실행 표면: `study/04-Network-Diagnostics-and-Routing/traceroute/problem/Makefile`
- 문제 문서 기준: canonical success criterion은 raw-socket free deterministic parser/formatter test다

## 핵심 코드 근거

- `build_probe_port()`: TTL/probe index/probes-per-hop를 이용해 collision 없는 UDP destination port를 만든다.
- `parse_icmp_response()`: raw ICMP packet 안의 embedded IP + UDP header에서 original probe port를 꺼낸다.
- `trace_route()`: raw ICMP receive socket과 UDP send socket을 분리하고, TTL마다 `ProbeObservation` 3개를 수집한다.
- 종료 조건: destination IP에서 `icmp_type == 3 and icmp_code == 3`이 관찰되면 route trace를 멈춘다.

## 테스트 근거

`make -C network-atda/study/04-Network-Diagnostics-and-Routing/traceroute/problem test`

결과:

- `4 passed in 0.01s`

세부:

- probe port mapping test 통과
- embedded UDP port parse test 통과
- hop formatting test 통과
- synthetic route integration test에서 3 hops 후 종료 확인
- live run target은 `make run-client HOST=8.8.8.8`로만 제공되고, 별도 live smoke script는 없다

보조 실행:

- `python3 python/src/traceroute.py example.com --max-hops 2 --probes 1 --timeout 0.2`은 현재 세션에서 5초 내 완료되지 않았다

## 이번에 고정한 해석

- 이 lab의 핵심은 TTL increment 자체보다 reply correlation을 port space로 안정화하는 데 있다.
- parser/unit tests가 훨씬 강한 근거이고, live path는 environment-dependent supplemental signal로 남겨야 한다.
- traceroute output formatting을 별도 함수로 분리한 덕분에 logic과 presentation이 깔끔하게 갈린다.
- 즉 현재 저장소는 intentionally "live traceroute correctness"보다 "parser/correlation determinism"을 canonical verification 대상으로 택한다.
