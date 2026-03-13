    # Series Map — RDT Protocol

    | 항목 | 내용 |
    | :--- | :--- |
    | 대상 프로젝트 | `02-Reliable-Transport/rdt-protocol` |
    | 문제 배경 | `Computer Networking: A Top-Down Approach`의 rdt3.0/GBN 흐름을 현재 저장소 구조에 맞게 정리한 구현 프로젝트 |
    | 공개 답안 표면 | `python/src/gbn.py`, `python/src/rdt3.py` |
    | 정식 검증 | `make -C study/02-Reliable-Transport/rdt-protocol/problem test` |
    | rewrite 방식 | `isolate-and-rewrite` |
    | legacy 보관 위치 | `_legacy/2026-03-13-isolate-and-rewrite/02-Reliable-Transport/rdt-protocol` |

    ## 프로젝트 경계
    - 이 프로젝트는 alternating-bit stop-and-wait에서 cumulative ACK 기반 Go-Back-N까지 넓혀 가는 신뢰 전송 시뮬레이션를 독립 문제로 다룬다.
    - `README.md`, `problem/`, `python/`, `docs/`가 한 폴더 아래에 닫혀 있어 다른 lab 없이도 범위 설명과 재검증이 가능하다.
    - canonical entrypoint는 `make -C study/02-Reliable-Transport/rdt-protocol/problem test`이며, 이번 재실행에서도 RDT Protocol Test Suite: RDT 3.0 transfer PASS, GBN transfer PASS 신호를 확인했다.

    ## 이번 rewrite의 입력 표면
    - `problem/code/channel.py`: 손실과 손상을 흉내 내는 비신뢰 채널
- `problem/code/packet.py`: 패킷 인코딩/디코딩 helper
- `problem/code/rdt3_skeleton.py`: rdt3.0 skeleton
- `problem/code/gbn_skeleton.py`: GBN skeleton
- `problem/data/test_messages.txt`: 테스트 메시지
- `problem/script/test_rdt.sh`: 정식 검증 스크립트
    - 소스 파일: `python/src/gbn.py`, `python/src/rdt3.py`
    - 테스트 파일: `python/tests/test_rdt.py`
    - `docs/concepts/gbn-vs-sr.md` - GBN vs Selective Repeat — 파이프라인 프로토콜 비교
- `docs/concepts/go-back-n.md` - Go-Back-N (GBN) Protocol
- `docs/concepts/rdt-principles.md` - Principles of Reliable Data Transfer
- `docs/concepts/rdt3.md` - RDT 3.0 — Alternating-Bit Protocol

    ## 이번 rewrite에서 제외한 입력
    - 기존 `study/blog/02-Reliable-Transport/rdt-protocol` 초안
    - `notion/`, `notion-archive/` 계열 노트
    - track 단위 회고나 다른 프로젝트 blog

    ## 이번 글에서 꼭 복원할 장면
    - Session 1: stop-and-wait baseline을 먼저 세웠다
- Session 2: Go-Back-N으로 window를 확장했다
- Session 3: 공유 harness와 비교 문서로 마감했다

    ## 이번 프로젝트가 남긴 학습 포인트
    - alternating bit와 cumulative ACK의 차이
- timeout 기반 재전송
- sliding window의 기본 구조
- 실제 네트워크 대신 시뮬레이션 채널에서 프로토콜을 검증하는 법
