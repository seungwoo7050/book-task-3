# Python 구현 안내

    이 디렉터리는 `UDP Pinger`의 공개 구현을 담습니다. 현재 저장소의 canonical 검증을 통과하는 범위를 기준으로 코드를 읽을 수 있게 정리합니다.

    ## 어디서부터 읽으면 좋은가

    1. `python/src/udp_pinger_client.py` - 핵심 구현 진입점입니다.
2. `python/tests/test_udp_pinger.py` - 검증 의도와 보조 테스트를 확인합니다.

    ## 기준 명령

    - 실행: `make -C study/Application-Protocols-and-Sockets/udp-pinger/problem run-solution`
- 검증: `make -C study/Application-Protocols-and-Sockets/udp-pinger/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

    ## 현재 범위

    UDP의 비연결성과 timeout 기반 손실 처리를 RTT 측정 과제로 묶은 구현입니다.

    ## 남은 약점

    - 패킷 순서 역전은 별도 처리하지 않습니다.
- 분위수 같은 고급 통계는 계산하지 않습니다.
- `pytest` 단독 실행은 제공 서버 선기동이 필요합니다.
