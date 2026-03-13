    # Series Map — UDP Pinger

    | 항목 | 내용 |
    | :--- | :--- |
    | 대상 프로젝트 | `01-Application-Protocols-and-Sockets/udp-pinger` |
    | 문제 배경 | `Computer Networking: A Top-Down Approach`의 UDP ping 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 |
    | 공개 답안 표면 | `python/src/udp_pinger_client.py` |
    | 정식 검증 | `make -C study/01-Application-Protocols-and-Sockets/udp-pinger/problem test` |
    | rewrite 방식 | `isolate-and-rewrite` |
    | legacy 보관 위치 | `_legacy/2026-03-13-isolate-and-rewrite/01-Application-Protocols-and-Sockets/udp-pinger` |

    ## 프로젝트 경계
    - 이 프로젝트는 10번의 UDP ping을 보내며 timeout, RTT, loss 통계를 함께 남기는 클라이언트를 독립 문제로 다룬다.
    - `README.md`, `problem/`, `python/`, `docs/`가 한 폴더 아래에 닫혀 있어 다른 lab 없이도 범위 설명과 재검증이 가능하다.
    - canonical entrypoint는 `make -C study/01-Application-Protocols-and-Sockets/udp-pinger/problem test`이며, 이번 재실행에서도 UDP Pinger Test Suite: ping 출력과 statistics 확인, 총 3 passed 신호를 확인했다.

    ## 이번 rewrite의 입력 표면
    - `problem/code/udp_pinger_server.py`: 손실을 시뮬레이션하는 제공 서버
- `problem/code/udp_pinger_client_skeleton.py`: 클라이언트 skeleton
- `problem/script/test_pinger.sh`: 정식 검증 스크립트
    - 소스 파일: `python/src/udp_pinger_client.py`
    - 테스트 파일: `python/tests/test_udp_pinger.py`
    - `docs/concepts/reproducibility.md` - 재현 가이드
- `docs/concepts/rtt.md` - Round-Trip Time (RTT) Measurement
- `docs/concepts/udp-sockets.md` - UDP Socket Programming in Python
- `docs/concepts/udp-vs-tcp.md` - UDP vs TCP 비교와 패킷 손실 처리

    ## 이번 rewrite에서 제외한 입력
    - 기존 `study/blog/01-Application-Protocols-and-Sockets/udp-pinger` 초안
    - `notion/`, `notion-archive/` 계열 노트
    - track 단위 회고나 다른 프로젝트 blog

    ## 이번 글에서 꼭 복원할 장면
    - Session 1: 실행 entrypoint와 최소 runtime surface를 먼저 고정했다
- Session 2: 핵심 protocol/algorithm branch를 채웠다
- Session 3: canonical test와 문서로 경계를 닫았다

    ## 이번 프로젝트가 남긴 학습 포인트
    - UDP의 connectionless socket 사용법
- 1초 timeout을 손실 판정으로 바꾸는 방법
- RTT 최소값/평균값/최대값과 손실률 계산
- ICMP ping과 UDP echo 과제의 차이 이해
