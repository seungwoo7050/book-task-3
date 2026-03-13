    # Series Map — ICMP Pinger

    | 항목 | 내용 |
    | :--- | :--- |
    | 대상 프로젝트 | `04-Network-Diagnostics-and-Routing/icmp-pinger` |
    | 문제 배경 | `Computer Networking: A Top-Down Approach`의 ICMP ping 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 |
    | 공개 답안 표면 | `python/src/icmp_pinger.py` |
    | 정식 검증 | `make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test` |
    | rewrite 방식 | `isolate-and-rewrite` |
    | legacy 보관 위치 | `_legacy/2026-03-13-isolate-and-rewrite/04-Network-Diagnostics-and-Routing/icmp-pinger` |

    ## 프로젝트 경계
    - 이 프로젝트는 RFC 1071 checksum, raw ICMP echo packet, IHL 기반 reply parse를 묶은 ping 구현를 독립 문제로 다룬다.
    - `README.md`, `problem/`, `python/`, `docs/`가 한 폴더 아래에 닫혀 있어 다른 lab 없이도 범위 설명과 재검증이 가능하다.
    - canonical entrypoint는 `make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test`이며, 이번 재실행에서도 pytest: `../python/tests` 11 passed; live raw-socket check는 sudo 별도 신호를 확인했다.

    ## 이번 rewrite의 입력 표면
    - `problem/code/icmp_pinger_skeleton.py`: 시작용 skeleton 코드
- `problem/script/test_icmp.sh`: live raw-socket 검증 스크립트
- `python/tests/test_icmp_pinger.py`: 비권한 deterministic 테스트
    - 소스 파일: `python/src/icmp_pinger.py`
    - 테스트 파일: `python/tests/test_icmp_pinger.py`
    - `docs/concepts/checksum.md` - Internet Checksum Algorithm (RFC 1071)
- `docs/concepts/icmp.md` - ICMP Protocol Reference
- `docs/concepts/ping-comparison.md` - ICMP Pinger vs 시스템 ping — 비교 분석
- `docs/concepts/raw-sockets.md` - Raw Sockets in Python

    ## 이번 rewrite에서 제외한 입력
    - 기존 `study/blog/04-Network-Diagnostics-and-Routing/icmp-pinger` 초안
    - `notion/`, `notion-archive/` 계열 노트
    - track 단위 회고나 다른 프로젝트 blog

    ## 이번 글에서 꼭 복원할 장면
    - Session 1: checksum과 Echo Request 형식을 먼저 고정했다
- Session 2: reply parse와 ping loop를 묶었다
- Session 3: fake raw socket test로 privilege 경계를 분리했다

    ## 이번 프로젝트가 남긴 학습 포인트
    - RFC 1071 인터넷 체크섬
- raw socket 권한 모델
- IP header length(`IHL`) 파싱
- binary packet build/parse 패턴
- fake-socket 기반 deterministic integration test 설계
