# TCP and UDP Packet Analysis evidence ledger

이 문서는 긴 본문을 읽기 전에, 세 단계에서 어떤 판단이 있었는지만 빠르게 붙들기 위한 압축본이다.

## Phase 1. 질문과 trace 범위를 먼저 세우기

- 당시 목표: `TCP and UDP Packet Analysis`를 어디서부터 읽어야 하는지 고정한다.
- 핵심 변경 단위: `study/03-Packet-Analysis-Top-Down/tcp-udp/problem/README.md`, `study/03-Packet-Analysis-Top-Down/tcp-udp/problem/Makefile`, `study/03-Packet-Analysis-Top-Down/tcp-udp/analysis/src/tcp-udp-analysis.md`
- 무슨 판단을 했는가: 어디서 실행하고 어디서 검증하는지 먼저 정하지 않으면 본문이 기능 요약으로 흘러갈 가능성이 컸다.
- 실행한 CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem help
  open-tcp               Open the TCP upload trace in Wireshark GUI
  open-udp               Open the UDP DNS trace in Wireshark GUI
  filter-handshake       Show the TCP 3-way handshake (SYN, SYN-ACK, ACK)
  filter-data            Show TCP data segments (payload > 0)
  filter-retransmissions Show TCP retransmissions
  filter-udp             Show all UDP packets from DNS trace
```
- 검증 신호:
  - `make help`만 봐도 이 프로젝트가 어떤 target으로 열리고 닫히는지 드러난다.
  - 이 단계에서의 역할: 응용 계층 랩 다음에 전송 계층의 상태와 오버헤드를 직접 관찰하면서, 이후 신뢰 전송 구현 트랙과 연결되는 근거를 쌓을 수 있습니다.
- 핵심 코드/trace 앵커: `study/03-Packet-Analysis-Top-Down/tcp-udp/analysis/src/tcp-udp-analysis.md`의 `## Part 1: TCP Segment Structure`
- 다음으로 넘어간 이유: 이제 어디를 읽어야 할지 정해졌으니, 실제로 판단이 몰린 함수나 trace section으로 내려갈 수 있었다.

## Phase 2. handshake와 data segment를 비교 가능한 근거로 정리하기

- 당시 목표: `TCP의 신뢰성 메커니즘과 UDP의 단순성을 같은 전송 계층 시야에서 비교하는 랩입니다.`를 실제 코드나 trace 근거에 붙여 본다.
- 핵심 변경 단위: `study/03-Packet-Analysis-Top-Down/tcp-udp/analysis/src/tcp-udp-analysis.md`
- 무슨 판단을 했는가: 전체 파일을 다 설명하기보다, 판단이 바뀐 줄 몇 개를 먼저 붙드는 편이 더 정확하다고 판단했다.
- 실행한 CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem filter-handshake
tshark -r data/tcp-upload.pcapng -Y "tcp.flags.syn == 1 || (tcp.flags.ack == 1 && tcp.seq == 1 && tcp.ack == 1)" \
3	192.168.0.2	128.119.245.12	54000	80	0x0010	1	1
4	192.168.0.2	128.119.245.12	54000	80	0x0018	1	1
```
- 검증 신호:
  - 이 출력만으로도 `## Part 2: TCP Connection Management` 주변이 설명의 중심축이라는 점이 드러난다.
  - relative sequence/ack 읽기
- 핵심 코드/trace 앵커: `study/03-Packet-Analysis-Top-Down/tcp-udp/analysis/src/tcp-udp-analysis.md`의 `## Part 2: TCP Connection Management`
- 다음으로 넘어간 이유: 중심 규칙을 잡은 뒤에는, 이 구현이나 분석이 실제로 무엇으로 닫히는지만 확인하면 됐다.

## Phase 3. verify 스크립트와 한계까지 정리하기

- 당시 목표: 통과 신호와 남은 범위를 한 번에 정리한다.
- 핵심 변경 단위: `study/03-Packet-Analysis-Top-Down/tcp-udp/analysis/src/tcp-udp-analysis.md`, `problem/script/`, `docs/`
- 무슨 판단을 했는가: 테스트 통과만 적으면 과장이 되기 쉬워서, 어디까지 확인됐고 무엇이 남는지도 같이 적어야 한다고 봤다.
- 실행한 CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem test
PASS: tcp-udp answer file passed content verification
```
- 검증 신호:
  - `make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem test`가 현재 공개 답안을 다시 재현해 준다.
  - trace가 짧아 전체 congestion window evolution을 직접 보기는 어렵습니다.
- 핵심 코드/trace 앵커: `study/03-Packet-Analysis-Top-Down/tcp-udp/analysis/src/tcp-udp-analysis.md`의 `## Part 3: UDP`
- 다음으로 넘어간 이유: 통과 신호와 경계가 모두 적혔으니, 긴 본문에서는 각 단계를 더 사람 읽기 좋게 풀어 쓰면 된다.
