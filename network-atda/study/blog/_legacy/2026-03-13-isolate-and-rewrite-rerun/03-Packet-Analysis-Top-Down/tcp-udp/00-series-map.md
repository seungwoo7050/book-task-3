    # Series Map — TCP and UDP Packet Analysis

    | 항목 | 내용 |
    | :--- | :--- |
    | 대상 프로젝트 | `03-Packet-Analysis-Top-Down/tcp-udp` |
    | 문제 배경 | `Computer Networking: A Top-Down Approach`의 TCP/UDP Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트 |
    | 공개 답안 표면 | `analysis/src/tcp-udp-analysis.md` |
    | 정식 검증 | `make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem test` |
    | rewrite 방식 | `isolate-and-rewrite` |
    | legacy 보관 위치 | `_legacy/2026-03-13-isolate-and-rewrite/03-Packet-Analysis-Top-Down/tcp-udp` |

    ## 프로젝트 경계
    - 이 프로젝트는 TCP 3-way handshake와 data segment, retransmission, UDP DNS datagram을 한 랩 안에서 대비시키는 trace 읽기를 독립 문제로 다룬다.
    - `README.md`, `problem/`, `analysis/`, `docs/`가 한 폴더 아래에 닫혀 있어 다른 lab 없이도 범위 설명과 재검증이 가능하다.
    - canonical entrypoint는 `make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem test`이며, 이번 재실행에서도 verify_answers.sh: `tcp-udp` answer file passed content verification 신호를 확인했다.

    ## 이번 rewrite의 입력 표면
    - `problem/data/tcp-upload.pcapng`: HTTP POST 업로드가 담긴 TCP trace
- `problem/data/udp-dns.pcapng`: DNS 질의/응답이 담긴 UDP trace
- `analysis/src/tcp-udp-analysis.md`: 공개 답안
    - 소스 파일: `analysis/src/tcp-udp-analysis.md`
    - 테스트는 `problem/script/*`와 canonical CLI를 중심으로 봤다.
    - `docs/concepts/reproducibility.md` - 재현 가이드
- `docs/concepts/tcp-flow-congestion.md` - TCP Flow Control and Congestion Control
- `docs/concepts/tcp-protocol.md` - TCP Protocol Reference
- `docs/concepts/tcp-retransmission.md` - TCP 재전송 메커니즘 심층 분석

    ## 이번 rewrite에서 제외한 입력
    - 기존 `study/blog/03-Packet-Analysis-Top-Down/tcp-udp` 초안
    - `notion/`, `notion-archive/` 계열 노트
    - track 단위 회고나 다른 프로젝트 blog

    ## 이번 글에서 꼭 복원할 장면
    - Session 1: trace inventory와 CLI filter surface를 먼저 고정했다
- Session 2: answer file을 파트 순서대로 채웠다
- Session 3: docs와 verify script로 근거를 정리했다

    ## 이번 프로젝트가 남긴 학습 포인트
    - 3-way handshake 해석
- relative sequence/ack 읽기
- window field와 retransmission 표시
- UDP의 8-byte header와 무상태성
