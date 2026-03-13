    # Structure Design — ICMP Pinger

    ## opening
    - 시작 질문: 이 프로젝트를 실제로 어디서부터 만들기 시작했는가.
    - 바로 보여 줄 증거: `make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test`와 ``python/src/icmp_pinger.py::internet_checksum``.
    - 서술 원칙: 결과 요약보다 Session별 판단 이동을 우선한다.
    - 메모: `make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test`가 통과하는 상태를 출발점으로 삼되, 실제 글의 첫 장면은 ``python/src/icmp_pinger.py::internet_checksum``에서 시작한다.

    ## Session 1 — checksum과 Echo Request 형식을 먼저 고정했다
- 다룰 파일/표면: `python/src/icmp_pinger.py::internet_checksum`, `python/src/icmp_pinger.py::build_echo_request`
- 글에서 먼저 던질 질문: "raw socket 문제의 첫 실패 지점은 OS 권한보다 잘못된 checksum일 가능성이 높다"
- 꼭 넣을 CLI: `make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test`
- 꼭 남길 검증 신호: packet 전체로 checksum을 다시 계산했을 때 0이 되는 테스트가 생겼다.
- 핵심 전환 문장: ICMP Echo는 header보다 payload에 timestamp를 어떻게 넣고 되읽느냐가 RTT 측정의 중심이다.
## Session 2 — reply parse와 ping loop를 묶었다
- 다룰 파일/표면: `python/src/icmp_pinger.py::parse_echo_reply`, `python/src/icmp_pinger.py::ping`
- 글에서 먼저 던질 질문: "IPv4 header 길이를 건너뛰지 않으면 sequence, identifier, payload timestamp를 믿을 수 없다"
- 꼭 넣을 CLI: `sudo make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test-live HOST=google.com`
- 꼭 남길 검증 신호: 성공 reply, timeout, loss statistics가 같은 출력 표면에 정리됐다.
- 핵심 전환 문장: RFC 1071 인터넷 체크섬
## Session 3 — fake raw socket test로 privilege 경계를 분리했다
- 다룰 파일/표면: `python/tests/test_icmp_pinger.py`, `problem/script/test_icmp.sh`
- 글에서 먼저 던질 질문: "live raw-socket 검증은 있어도, 회귀는 fake socket 기반 deterministic test가 담당해야 한다"
- 꼭 넣을 CLI: `make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test`
- 꼭 남길 검증 신호: pytest: `../python/tests` 11 passed; live raw-socket check는 sudo 별도
- 핵심 전환 문장: raw socket 권한 모델

    ## ending
    - 마지막 단락에서는 현재 한계를 README bullet 그대로 축약해 남긴다.
    - IPv6/ICMPv6는 지원하지 않습니다.
- 시스템 `ping` 수준의 상세 통계는 제공하지 않습니다.
- live raw-socket 실행은 OS와 방화벽 정책에 영향을 받습니다.
