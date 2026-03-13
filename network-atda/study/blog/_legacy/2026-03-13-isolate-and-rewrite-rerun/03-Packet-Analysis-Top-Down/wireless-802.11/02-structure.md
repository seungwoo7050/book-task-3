    # Structure Design — 802.11 Wireless Packet Analysis

    ## opening
    - 시작 질문: 이 프로젝트를 실제로 어디서부터 만들기 시작했는가.
    - 바로 보여 줄 증거: `make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem test`와 ``analysis/src/wireless-analysis.md``.
    - 서술 원칙: 결과 요약보다 Session별 판단 이동을 우선한다.
    - 메모: `make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem test`가 통과하는 상태를 출발점으로 삼되, 실제 글의 첫 장면은 ``analysis/src/wireless-analysis.md``에서 시작한다.

    ## Session 1 — trace inventory와 CLI filter surface를 먼저 고정했다
- 다룰 파일/표면: `problem/Makefile`, `analysis/src/wireless-analysis.md`
- 글에서 먼저 던질 질문: "analysis 프로젝트도 구현 프로젝트처럼 먼저 entrypoint를 잡지 않으면 chronology가 흐려진다"
- 꼭 넣을 CLI: `make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem beacons`
- 꼭 남길 검증 신호: 어떤 질문이 어떤 trace와 filter에 기대는지 다시 찾아갈 수 있는 표면이 생겼다.
- 핵심 전환 문장: management/control/data frame 분류
## Session 2 — answer file을 파트 순서대로 채웠다
- 다룰 파일/표면: `analysis/src/wireless-analysis.md`의 `Part 1: Beacon Frames (Q1–Q5)` / `Part 2: Probe Request and Response (Q6–Q9)` / Part 3: Authentication and Association (Q10–Q14) and Part 4: Data Frames and Structure (Q15–Q18)
- 글에서 먼저 던질 질문: "가장 눈에 띄는 frame만 적으면 설명이 편해 보이지만, part 순서대로 답을 채워야 문제 범위가 유지된다"
- 꼭 넣을 CLI: `make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem probes`
- 꼭 남길 검증 신호: analysis/src 답안이 문제의 part ordering과 같은 순서로 닫히기 시작했다.
- 핵심 전환 문장: beacon과 probe의 의미
## Session 3 — docs와 verify script로 근거를 정리했다
- 다룰 파일/표면: `docs/concepts/802.11-frame-format.md`, `docs/concepts/wifi-security-evolution.md`, `problem/script/verify_answers.sh`
- 글에서 먼저 던질 질문: "analysis 글도 마지막에 `무엇을 봤는가`뿐 아니라 `어떤 개념으로 읽었는가`를 남겨야 다음 trace로 이어진다"
- 꼭 넣을 CLI: `make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem test`
- 꼭 남길 검증 신호: verify_answers.sh: `wireless-802.11` answer file passed content verification
- 핵심 전환 문장: management/control/data frame 분류 and beacon과 probe의 의미

    ## ending
    - 마지막 단락에서는 현재 한계를 README bullet 그대로 축약해 남긴다.
    - compact synthetic trace라 실제 monitor-mode 캡처보다 단순화된 부분이 있습니다.
- EAPOL/WPA handshake 심화는 포함하지 않습니다.
- 실제 RF 잡음과 retry 패턴은 제한적으로만 보입니다.
