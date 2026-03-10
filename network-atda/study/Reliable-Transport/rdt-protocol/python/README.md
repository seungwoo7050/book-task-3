# Python 구현 안내

    이 디렉터리는 `RDT Protocol`의 공개 구현을 담습니다. 현재 저장소의 canonical 검증을 통과하는 범위를 기준으로 코드를 읽을 수 있게 정리합니다.

    ## 어디서부터 읽으면 좋은가

    1. `python/src/gbn.py` - 핵심 구현 진입점입니다.
2. `python/src/rdt3.py` - 핵심 구현 진입점입니다.
3. `python/tests/test_rdt.py` - 검증 의도와 보조 테스트를 확인합니다.

    ## 기준 명령

    - 실행: `make -C study/Reliable-Transport/rdt-protocol/problem run-solution-rdt3`
- 검증: `make -C study/Reliable-Transport/rdt-protocol/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

    ## 현재 범위

    `rdt3.0`과 `Go-Back-N`을 같은 채널 모델 위에서 비교하는 신뢰 전송 과제입니다.

    ## 남은 약점

    - 실제 네트워크가 아니라 시뮬레이션 채널을 사용합니다.
- GBN 성능 로그를 자동 수집하지 않습니다.
- 동시성 대신 단일 이벤트 루프를 사용합니다.
