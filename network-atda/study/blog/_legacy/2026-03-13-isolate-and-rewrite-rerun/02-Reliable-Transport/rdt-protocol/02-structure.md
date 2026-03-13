    # Structure Design — RDT Protocol

    ## opening
    - 시작 질문: 이 프로젝트를 실제로 어디서부터 만들기 시작했는가.
    - 바로 보여 줄 증거: `make -C study/02-Reliable-Transport/rdt-protocol/problem test`와 ``python/src/rdt3.py::rdt_send_receive``.
    - 서술 원칙: 결과 요약보다 Session별 판단 이동을 우선한다.
    - 메모: `make -C study/02-Reliable-Transport/rdt-protocol/problem test`가 통과하는 상태를 출발점으로 삼되, 실제 글의 첫 장면은 ``python/src/rdt3.py::rdt_send_receive``에서 시작한다.

    ## Session 1 — stop-and-wait baseline을 먼저 세웠다
- 다룰 파일/표면: `python/src/rdt3.py::rdt_send_receive`, `problem/code/packet.py`, `problem/code/channel.py`
- 글에서 먼저 던질 질문: "reliable transfer의 최소 단위는 alternating-bit와 timeout 조합일 것이다"
- 꼭 넣을 CLI: `make -C study/02-Reliable-Transport/rdt-protocol/problem run-solution-rdt3`
- 꼭 남길 검증 신호: rdt3 demo surface가 생기면서 sender/receiver 로그를 sequence 단위로 읽을 수 있게 됐다.
- 핵심 전환 문장: sequence number 하나만 있어도 duplicate와 ACK loss를 구분할 수 있다.
## Session 2 — Go-Back-N으로 window를 확장했다
- 다룰 파일/표면: `python/src/gbn.py::gbn_send_receive`
- 글에서 먼저 던질 질문: "cumulative ACK를 받으면 base만 앞으로 밀고 timeout 시 base..next_seq-1 전체를 다시 보내면 된다"
- 꼭 넣을 CLI: `make -C study/02-Reliable-Transport/rdt-protocol/problem run-solution-gbn`
- 꼭 남길 검증 신호: GBN demo가 loss/corruption 환경에서도 전체 메시지를 끝까지 전달했다.
- 핵심 전환 문장: GBN의 단순함은 수신측 버퍼를 포기하고 송신측 재전송 범위를 넓게 잡는 데서 나온다.
## Session 3 — 공유 harness와 비교 문서로 마감했다
- 다룰 파일/표면: `problem/script/test_rdt.sh`, `python/tests/test_rdt.py`, `docs/concepts/gbn-vs-sr.md`
- 글에서 먼저 던질 질문: "CLI가 sequence 로그를 그대로 보여 줘야 chronology도 과장되지 않는다"
- 꼭 넣을 CLI: `make -C study/02-Reliable-Transport/rdt-protocol/problem test`
- 꼭 남길 검증 신호: RDT Protocol Test Suite: RDT 3.0 transfer PASS, GBN transfer PASS
- 핵심 전환 문장: alternating bit와 cumulative ACK의 차이

    ## ending
    - 마지막 단락에서는 현재 한계를 README bullet 그대로 축약해 남긴다.
    - 실제 네트워크가 아니라 시뮬레이션 채널을 사용합니다.
- GBN 성능 로그를 자동 수집하지 않습니다.
- 동시성 대신 단일 이벤트 루프를 사용합니다.
