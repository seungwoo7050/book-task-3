    # Series Map — Traceroute

    | 항목 | 내용 |
    | :--- | :--- |
    | 대상 프로젝트 | `04-Network-Diagnostics-and-Routing/traceroute` |
    | 문제 배경 | ICMP/TTL 학습을 실제 경로 추적 도구로 연결하기 위해 이 저장소에서 직접 보강한 bridge 프로젝트 |
    | 공개 답안 표면 | `python/src/traceroute.py` |
    | 정식 검증 | `make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem test` |
    | rewrite 방식 | `isolate-and-rewrite` |
    | legacy 보관 위치 | `_legacy/2026-03-13-isolate-and-rewrite/04-Network-Diagnostics-and-Routing/traceroute` |

    ## 프로젝트 경계
    - 이 프로젝트는 TTL을 올려 가며 UDP probe를 보내고 embedded UDP port로 ICMP reply를 매칭하는 traceroute 구현를 독립 문제로 다룬다.
    - `README.md`, `problem/`, `python/`, `docs/`가 한 폴더 아래에 닫혀 있어 다른 lab 없이도 범위 설명과 재검증이 가능하다.
    - canonical entrypoint는 `make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem test`이며, 이번 재실행에서도 pytest: `../python/tests` 4 passed 신호를 확인했다.

    ## 이번 rewrite의 입력 표면
    - `problem/code/traceroute_skeleton.py`: 시작용 skeleton 코드
- `python/src/traceroute.py`: 현재 공개 구현
- `python/tests/test_traceroute.py`: 비권한 parser + synthetic route 테스트
    - 소스 파일: `python/src/traceroute.py`
    - 테스트 파일: `python/tests/test_traceroute.py`
    - `docs/concepts/icmp-protocol.md` - ICMP Protocol Reference
- `docs/concepts/ipv4-header.md` - IPv4 Header Reference
- `docs/concepts/raw-sockets.md` - Raw Sockets in Python

    ## 이번 rewrite에서 제외한 입력
    - 기존 `study/blog/04-Network-Diagnostics-and-Routing/traceroute` 초안
    - `notion/`, `notion-archive/` 계열 노트
    - track 단위 회고나 다른 프로젝트 blog

    ## 이번 글에서 꼭 복원할 장면
    - Session 1: probe를 식별할 포트 규칙부터 정했다
- Session 2: TTL loop와 hop line 출력을 완성했다
- Session 3: synthetic route test로 출력 contract를 잠갔다

    ## 이번 프로젝트가 남긴 학습 포인트
    - TTL과 `ICMP Time Exceeded`의 연결
- embedded UDP port를 이용한 probe 매칭
- live probing과 synthetic integration test 분리
- 목적지 도달을 `Port Unreachable`로 판정하는 규칙
