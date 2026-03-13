    # Structure Design — Traceroute

    ## opening
    - 시작 질문: 이 프로젝트를 실제로 어디서부터 만들기 시작했는가.
    - 바로 보여 줄 증거: `make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem test`와 ``python/src/traceroute.py::parse_icmp_response``.
    - 서술 원칙: 결과 요약보다 Session별 판단 이동을 우선한다.
    - 메모: `make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem test`가 통과하는 상태를 출발점으로 삼되, 실제 글의 첫 장면은 ``python/src/traceroute.py::parse_icmp_response``에서 시작한다.

    ## Session 1 — probe를 식별할 포트 규칙부터 정했다
- 다룰 파일/표면: `python/src/traceroute.py::build_probe_port`, `python/src/traceroute.py::parse_icmp_response`
- 글에서 먼저 던질 질문: "traceroute에서 가장 먼저 흔들리는 부분은 어떤 ICMP reply가 어떤 probe의 것인지 매칭하는 규칙이다"
- 꼭 넣을 CLI: `make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem run-client HOST=8.8.8.8`
- 꼭 남길 검증 신호: synthetic packet에서도 `(icmp_type, icmp_code, dest_port)`를 안정적으로 추출할 수 있게 됐다.
- 핵심 전환 문장: hop discovery는 TTL 자체보다 embedded original datagram을 다시 읽는 parsing에서 성패가 갈린다.
## Session 2 — TTL loop와 hop line 출력을 완성했다
- 다룰 파일/표면: `python/src/traceroute.py::trace_route`, `python/src/traceroute.py::format_hop_line`
- 글에서 먼저 던질 질문: "각 hop은 probe 3개를 모아서 `*`와 responder IP를 함께 보여 줘야 실제 traceroute처럼 읽힌다"
- 꼭 넣을 CLI: `make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem run-client HOST=8.8.8.8`
- 꼭 남길 검증 신호: header line과 hop line 목록이 완성되면서 synthetic route에서도 1 hop씩 출력할 수 있게 됐다.
- 핵심 전환 문장: TTL과 `ICMP Time Exceeded`의 연결
## Session 3 — synthetic route test로 출력 contract를 잠갔다
- 다룰 파일/표면: `python/tests/test_traceroute.py`
- 글에서 먼저 던질 질문: "live network보다 fake ICMP route map이 regression에는 더 강하다"
- 꼭 넣을 CLI: `make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem test`
- 꼭 남길 검증 신호: pytest: `../python/tests` 4 passed
- 핵심 전환 문장: embedded UDP port를 이용한 probe 매칭

    ## ending
    - 마지막 단락에서는 현재 한계를 README bullet 그대로 축약해 남긴다.
    - IPv6 traceroute는 지원하지 않습니다.
- DNS reverse lookup은 포함하지 않습니다.
- ECMP나 비대칭 경로 같은 실제 인터넷 변동성은 모델링하지 않습니다.
