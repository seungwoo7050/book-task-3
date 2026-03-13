    # Series Map — 802.11 Wireless Packet Analysis

    | 항목 | 내용 |
    | :--- | :--- |
    | 대상 프로젝트 | `03-Packet-Analysis-Top-Down/wireless-802.11` |
    | 문제 배경 | `Computer Networking: A Top-Down Approach`의 802.11 Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트 |
    | 공개 답안 표면 | `analysis/src/wireless-analysis.md` |
    | 정식 검증 | `make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem test` |
    | rewrite 방식 | `isolate-and-rewrite` |
    | legacy 보관 위치 | `_legacy/2026-03-13-isolate-and-rewrite/03-Packet-Analysis-Top-Down/wireless-802.11` |

    ## 프로젝트 경계
    - 이 프로젝트는 beacon, probe, authentication, association, data, ACK까지 802.11 frame subtype 흐름을 읽는 wireless trace 분석를 독립 문제로 다룬다.
    - `README.md`, `problem/`, `analysis/`, `docs/`가 한 폴더 아래에 닫혀 있어 다른 lab 없이도 범위 설명과 재검증이 가능하다.
    - canonical entrypoint는 `make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem test`이며, 이번 재실행에서도 verify_answers.sh: `wireless-802.11` answer file passed content verification 신호를 확인했다.

    ## 이번 rewrite의 입력 표면
    - `problem/data/wireless-trace.pcap`: 802.11 monitor mode trace
- `analysis/src/wireless-analysis.md`: 공개 답안
- `docs/concepts/802.11-frame-format.md`: 802.11 프레임 개념 문서
    - 소스 파일: `analysis/src/wireless-analysis.md`
    - 테스트는 `problem/script/*`와 canonical CLI를 중심으로 봤다.
    - `docs/concepts/802.11-frame-format.md` - IEEE 802.11 Frame Format
- `docs/concepts/wifi-security-evolution.md` - Wi-Fi 보안 프로토콜의 진화: WEP → WPA → WPA2 → WPA3
- `docs/concepts/wireless-management.md` - Wireless Management Frames
- `docs/concepts/wireshark-wireless.md` - Wireshark Wireless Analysis Techniques

    ## 이번 rewrite에서 제외한 입력
    - 기존 `study/blog/03-Packet-Analysis-Top-Down/wireless-802.11` 초안
    - `notion/`, `notion-archive/` 계열 노트
    - track 단위 회고나 다른 프로젝트 blog

    ## 이번 글에서 꼭 복원할 장면
    - Session 1: trace inventory와 CLI filter surface를 먼저 고정했다
- Session 2: answer file을 파트 순서대로 채웠다
- Session 3: docs와 verify script로 근거를 정리했다

    ## 이번 프로젝트가 남긴 학습 포인트
    - management/control/data frame 분류
- beacon과 probe의 의미
- authentication -> association 절차
- `To DS`/`From DS`와 주소 field 해석
