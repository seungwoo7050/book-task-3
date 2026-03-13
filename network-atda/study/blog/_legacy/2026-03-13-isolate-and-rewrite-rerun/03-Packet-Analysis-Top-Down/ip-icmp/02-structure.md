    # Structure Design — IP and ICMP Packet Analysis

    ## opening
    - 시작 질문: 이 프로젝트를 실제로 어디서부터 만들기 시작했는가.
    - 바로 보여 줄 증거: `make -C study/03-Packet-Analysis-Top-Down/ip-icmp/problem test`와 ``analysis/src/ip-icmp-analysis.md``.
    - 서술 원칙: 결과 요약보다 Session별 판단 이동을 우선한다.
    - 메모: `make -C study/03-Packet-Analysis-Top-Down/ip-icmp/problem test`가 통과하는 상태를 출발점으로 삼되, 실제 글의 첫 장면은 ``analysis/src/ip-icmp-analysis.md``에서 시작한다.

    ## Session 1 — trace inventory와 CLI filter surface를 먼저 고정했다
- 다룰 파일/표면: `problem/Makefile`, `analysis/src/ip-icmp-analysis.md`
- 글에서 먼저 던질 질문: "analysis 프로젝트도 구현 프로젝트처럼 먼저 entrypoint를 잡지 않으면 chronology가 흐려진다"
- 꼭 넣을 CLI: `make -C study/03-Packet-Analysis-Top-Down/ip-icmp/problem filter-icmp`
- 꼭 남길 검증 신호: 어떤 질문이 어떤 trace와 filter에 기대는지 다시 찾아갈 수 있는 표면이 생겼다.
- 핵심 전환 문장: IPv4 header field 해석
## Session 2 — answer file을 파트 순서대로 채웠다
- 다룰 파일/표면: `analysis/src/ip-icmp-analysis.md`의 `Part 1: IPv4 Header` / `Part 2: IP Fragmentation` / Part 3: ICMP Messages
- 글에서 먼저 던질 질문: "가장 눈에 띄는 frame만 적으면 설명이 편해 보이지만, part 순서대로 답을 채워야 문제 범위가 유지된다"
- 꼭 넣을 CLI: `make -C study/03-Packet-Analysis-Top-Down/ip-icmp/problem filter-fragments`
- 꼭 남길 검증 신호: analysis/src 답안이 문제의 part ordering과 같은 순서로 닫히기 시작했다.
- 핵심 전환 문장: fragmentation 3요소(`Identification`, `Flags`, `Offset`)
## Session 3 — docs와 verify script로 근거를 정리했다
- 다룰 파일/표면: `docs/concepts/icmp-protocol.md`, `docs/concepts/ipv4-header.md`, `problem/script/verify_answers.sh`
- 글에서 먼저 던질 질문: "analysis 글도 마지막에 `무엇을 봤는가`뿐 아니라 `어떤 개념으로 읽었는가`를 남겨야 다음 trace로 이어진다"
- 꼭 넣을 CLI: `make -C study/03-Packet-Analysis-Top-Down/ip-icmp/problem test`
- 꼭 남길 검증 신호: verify_answers.sh: `ip-icmp` answer file passed content verification
- 핵심 전환 문장: IPv4 header field 해석 and fragmentation 3요소(`Identification`, `Flags`, `Offset`)

    ## ending
    - 마지막 단락에서는 현재 한계를 README bullet 그대로 축약해 남긴다.
    - IPv4 중심이며 IPv6 비교는 개념 문서에서만 다룹니다.
- OS별 traceroute 구현 차이는 실험하지 않습니다.
