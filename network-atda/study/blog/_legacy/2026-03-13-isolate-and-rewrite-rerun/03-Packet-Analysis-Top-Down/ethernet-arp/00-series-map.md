    # Series Map — Ethernet and ARP Packet Analysis

    | 항목 | 내용 |
    | :--- | :--- |
    | 대상 프로젝트 | `03-Packet-Analysis-Top-Down/ethernet-arp` |
    | 문제 배경 | `Computer Networking: A Top-Down Approach`의 Ethernet/ARP Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트 |
    | 공개 답안 표면 | `analysis/src/ethernet-arp-analysis.md` |
    | 정식 검증 | `make -C study/03-Packet-Analysis-Top-Down/ethernet-arp/problem test` |
    | rewrite 방식 | `isolate-and-rewrite` |
    | legacy 보관 위치 | `_legacy/2026-03-13-isolate-and-rewrite/03-Packet-Analysis-Top-Down/ethernet-arp` |

    ## 프로젝트 경계
    - 이 프로젝트는 Ethernet header와 ARP request/reply, broadcast, ARP cache를 link-layer evidence로 고정하는 랩를 독립 문제로 다룬다.
    - `README.md`, `problem/`, `analysis/`, `docs/`가 한 폴더 아래에 닫혀 있어 다른 lab 없이도 범위 설명과 재검증이 가능하다.
    - canonical entrypoint는 `make -C study/03-Packet-Analysis-Top-Down/ethernet-arp/problem test`이며, 이번 재실행에서도 verify_answers.sh: `ethernet-arp` answer file passed content verification 신호를 확인했다.

    ## 이번 rewrite의 입력 표면
    - `problem/data/ethernet-arp.pcapng`: Ethernet/ARP trace
- `analysis/src/ethernet-arp-analysis.md`: 공개 답안
- `docs/concepts/arp-protocol.md`: ARP 개념 문서
    - 소스 파일: `analysis/src/ethernet-arp-analysis.md`
    - 테스트는 `problem/script/*`와 canonical CLI를 중심으로 봤다.
    - `docs/concepts/arp-protocol.md` - ARP Protocol Reference
- `docs/concepts/arp-security-switching.md` - ARP 보안 위협과 LAN 스위칭 심화
- `docs/concepts/ethernet-frame.md` - Ethernet Frame Reference
- `docs/concepts/wireshark-link.md` - Wireshark Link Layer Analysis Techniques

    ## 이번 rewrite에서 제외한 입력
    - 기존 `study/blog/03-Packet-Analysis-Top-Down/ethernet-arp` 초안
    - `notion/`, `notion-archive/` 계열 노트
    - track 단위 회고나 다른 프로젝트 blog

    ## 이번 글에서 꼭 복원할 장면
    - Session 1: trace inventory와 CLI filter surface를 먼저 고정했다
- Session 2: answer file을 파트 순서대로 채웠다
- Session 3: docs와 verify script로 근거를 정리했다

    ## 이번 프로젝트가 남긴 학습 포인트
    - EtherType와 상위 프로토콜 연결
- ARP request broadcast / reply unicast
- 게이트웨이 MAC 해석
- ARP 보안 취약점의 기본 개념
