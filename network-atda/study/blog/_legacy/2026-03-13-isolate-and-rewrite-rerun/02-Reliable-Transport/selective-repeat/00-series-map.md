    # Series Map — Selective Repeat

    | 항목 | 내용 |
    | :--- | :--- |
    | 대상 프로젝트 | `02-Reliable-Transport/selective-repeat` |
    | 문제 배경 | 이 저장소에서 `Go-Back-N` 다음 단계 학습을 위해 직접 보강한 Selective Repeat 프로젝트 |
    | 공개 답안 표면 | `python/src/selective_repeat.py` |
    | 정식 검증 | `make -C study/02-Reliable-Transport/selective-repeat/problem test` |
    | rewrite 방식 | `isolate-and-rewrite` |
    | legacy 보관 위치 | `_legacy/2026-03-13-isolate-and-rewrite/02-Reliable-Transport/selective-repeat` |

    ## 프로젝트 경계
    - 이 프로젝트는 packet별 timer와 receiver buffer로 selective retransmission을 구현하는 sliding-window 확장를 독립 문제로 다룬다.
    - `README.md`, `problem/`, `python/`, `docs/`가 한 폴더 아래에 닫혀 있어 다른 lab 없이도 범위 설명과 재검증이 가능하다.
    - canonical entrypoint는 `make -C study/02-Reliable-Transport/selective-repeat/problem test`이며, 이번 재실행에서도 Selective Repeat Test Suite: 전체 전달 PASS, selective retransmit 확인 PASS 신호를 확인했다.

    ## 이번 rewrite의 입력 표면
    - `problem/code/channel.py`: `rdt-protocol`과 공유하는 채널 helper
- `problem/code/packet.py`: 공유 packet helper
- `problem/code/selective_repeat_skeleton.py`: Selective Repeat skeleton
- `problem/data/test_messages.txt`: 테스트 메시지
- `problem/script/test_selective_repeat.sh`: 정식 검증 스크립트
    - 소스 파일: `python/src/selective_repeat.py`
    - 테스트 파일: `python/tests/test_selective_repeat.py`
    - `docs/concepts/gbn-vs-sr.md` - GBN vs Selective Repeat — 파이프라인 프로토콜 비교
- `docs/concepts/rdt-principles.md` - Principles of Reliable Data Transfer

    ## 이번 rewrite에서 제외한 입력
    - 기존 `study/blog/02-Reliable-Transport/selective-repeat` 초안
    - `notion/`, `notion-archive/` 계열 노트
    - track 단위 회고나 다른 프로젝트 blog

    ## 이번 글에서 꼭 복원할 장면
    - Session 1: 송신측을 packet별 timer 기준으로 다시 쪼갰다
- Session 2: receiver buffer와 in-order delivery를 붙였다
- Session 3: message fixture와 test로 재전송 경계를 고정했다

    ## 이번 프로젝트가 남긴 학습 포인트
    - 패킷별 timer 관리
- 수신 버퍼와 in-order delivery
- ACKed 집합과 sender base 업데이트
- GBN과 SR의 효율 차이 비교
