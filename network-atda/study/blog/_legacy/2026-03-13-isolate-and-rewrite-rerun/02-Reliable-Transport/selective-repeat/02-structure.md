    # Structure Design — Selective Repeat

    ## opening
    - 시작 질문: 이 프로젝트를 실제로 어디서부터 만들기 시작했는가.
    - 바로 보여 줄 증거: `make -C study/02-Reliable-Transport/selective-repeat/problem test`와 ``python/src/selective_repeat.py::selective_repeat_send_receive``.
    - 서술 원칙: 결과 요약보다 Session별 판단 이동을 우선한다.
    - 메모: `make -C study/02-Reliable-Transport/selective-repeat/problem test`가 통과하는 상태를 출발점으로 삼되, 실제 글의 첫 장면은 ``python/src/selective_repeat.py::selective_repeat_send_receive``에서 시작한다.

    ## Session 1 — 송신측을 packet별 timer 기준으로 다시 쪼갰다
- 다룰 파일/표면: `python/src/selective_repeat.py::selective_repeat_send_receive`의 sender 상태
- 글에서 먼저 던질 질문: "Selective Repeat의 핵심은 `send_base`보다 `acked`와 `timers`를 별도로 두는 것이다"
- 꼭 넣을 CLI: `make -C study/02-Reliable-Transport/selective-repeat/problem run-solution`
- 꼭 남길 검증 신호: loss/corruption 설정에서도 특정 sequence만 골라 재전송할 수 있는 표면이 생겼다.
- 핵심 전환 문장: window protocol에서 상태 공간이 늘어나는 지점은 sender보다 ACK bookkeeping이다.
## Session 2 — receiver buffer와 in-order delivery를 붙였다
- 다룰 파일/표면: `python/src/selective_repeat.py::selective_repeat_send_receive`의 receiver 상태
- 글에서 먼저 던질 질문: "GBN과 달리 out-of-order packet을 저장해야 selective retransmission의 이점이 살아난다"
- 꼭 넣을 CLI: `make -C study/02-Reliable-Transport/selective-repeat/problem run-solution`
- 꼭 남길 검증 신호: buffered seq와 delivered seq 로그가 분리되면서 receiver 동작이 눈에 보이기 시작했다.
- 핵심 전환 문장: Selective Repeat는 송신측 timer만 늘리는 게 아니라 수신측 reorder buffer까지 책임져야 완성된다.
## Session 3 — message fixture와 test로 재전송 경계를 고정했다
- 다룰 파일/표면: `problem/script/test_selective_repeat.sh`, `python/tests/test_selective_repeat.py`
- 글에서 먼저 던질 질문: "transfer 성공만 보지 말고 fixture 존재 여부와 무손실 경로도 같이 잠가야 한다"
- 꼭 넣을 CLI: `make -C study/02-Reliable-Transport/selective-repeat/problem test`
- 꼭 남길 검증 신호: Selective Repeat Test Suite: 전체 전달 PASS, selective retransmit 확인 PASS
- 핵심 전환 문장: 패킷별 timer 관리

    ## ending
    - 마지막 단락에서는 현재 한계를 README bullet 그대로 축약해 남긴다.
    - 실제 병렬 스레드 모델은 아닙니다.
- sequence wraparound는 구현하지 않았습니다.
- 성능 비교 표는 아직 정리하지 않았습니다.
