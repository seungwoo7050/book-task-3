# Python 구현 안내

    이 디렉터리는 `Distance-Vector Routing`의 공개 구현을 담습니다. 현재 저장소의 canonical 검증을 통과하는 범위를 기준으로 코드를 읽을 수 있게 정리합니다.

    ## 어디서부터 읽으면 좋은가

    1. `python/src/dv_routing.py` - 핵심 구현 진입점입니다.
2. `python/tests/test_dv_routing.py` - 검증 의도와 보조 테스트를 확인합니다.

    ## 기준 명령

    - 실행: `make -C study/Network-Diagnostics-and-Routing/routing/problem run-solution`
- 검증: `make -C study/Network-Diagnostics-and-Routing/routing/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

    ## 현재 범위

    Bellman-Ford 식을 분산 라우팅 테이블 갱신으로 옮기는 시뮬레이션 과제입니다.

    ## 남은 약점

    - poisoned reverse는 구현하지 않았습니다.
- 동적 토폴로지 변화 실험은 포함하지 않습니다.
- 비동기 메시지 모델은 구현하지 않습니다.
