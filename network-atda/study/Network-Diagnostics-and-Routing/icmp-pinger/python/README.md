# Python 구현 안내

    이 디렉터리는 `ICMP Pinger`의 공개 구현을 담습니다. 현재 저장소의 canonical 검증을 통과하는 범위를 기준으로 코드를 읽을 수 있게 정리합니다.

    ## 어디서부터 읽으면 좋은가

    1. `python/src/icmp_pinger.py` - 핵심 구현 진입점입니다.
2. `python/tests/test_icmp_pinger.py` - 검증 의도와 보조 테스트를 확인합니다.

    ## 기준 명령

    - 실행: `make -C study/Network-Diagnostics-and-Routing/icmp-pinger/problem run-solution HOST=google.com`
- 검증: `make -C study/Network-Diagnostics-and-Routing/icmp-pinger/problem test`
- 수동 live 검증: `sudo make -C study/Network-Diagnostics-and-Routing/icmp-pinger/problem test-live HOST=google.com`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

    ## 현재 범위

    Raw socket으로 `ICMP Echo Request/Reply`를 직접 구현하는 진단 도구 과제입니다.

    ## 남은 약점

    - IPv6/ICMPv6는 지원하지 않습니다.
- 시스템 `ping` 수준의 상세 통계는 제공하지 않습니다.
- live raw-socket 실행은 OS와 방화벽 정책에 영향을 받습니다.
