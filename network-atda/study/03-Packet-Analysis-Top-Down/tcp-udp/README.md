# TCP and UDP Packet Analysis

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 TCP/UDP Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트 |
| 정식 검증 | `make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem test` |

## 문제가 뭐였나
- 문제 배경: `Computer Networking: A Top-Down Approach`의 TCP/UDP Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트
- 이 단계에서의 역할: 응용 계층 랩 다음에 전송 계층의 상태와 오버헤드를 직접 관찰하면서, 이후 신뢰 전송 구현 트랙과 연결되는 근거를 쌓을 수 있습니다.

## 제공된 자료
- `problem/data/tcp-upload.pcapng`: HTTP POST 업로드가 담긴 TCP trace
- `problem/data/udp-dns.pcapng`: DNS 질의/응답이 담긴 UDP trace
- `analysis/src/tcp-udp-analysis.md`: 공개 답안

## 이 레포의 답
- 한 줄 답: TCP의 신뢰성 메커니즘과 UDP의 단순성을 같은 전송 계층 시야에서 비교하는 랩입니다.
- 공개 답안 위치: `analysis/src/`
- 보조 공개 표면: `docs/`
- 보조 공개 표면: `study/blog/03-Packet-Analysis-Top-Down/tcp-udp/`
- 읽는 순서:
  1. `problem/README.md` - 문제 조건, 제공 자료, 성공 기준을 먼저 확인합니다.
  2. `analysis/README.md` - 현재 공개 답안 범위와 기준 명령을 확인합니다.
  3. `../../blog/03-Packet-Analysis-Top-Down/tcp-udp/README.md` - 소스 기준의 분석 chronology를 따라갑니다.
  4. `docs/README.md` - 반복해서 참고할 개념 문서를 고릅니다.

## 어떻게 검증하나
- 검증: `make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem test`
- 공개 답안 위치: `analysis/src/`
- 개념 노트 위치: `docs/concepts/`

## 무엇을 배웠나
- 3-way handshake 해석
- relative sequence/ack 읽기
- window field와 retransmission 표시
- UDP의 8-byte header와 무상태성

## 현재 한계
- trace가 짧아 전체 congestion window evolution을 직접 보기는 어렵습니다.
- teardown과 장기 혼잡 제어 관찰은 제한적입니다.
