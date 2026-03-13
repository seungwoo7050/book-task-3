# IP and ICMP Packet Analysis evidence ledger

이 문서는 긴 본문을 읽기 전에, 세 단계에서 어떤 판단이 있었는지만 빠르게 붙들기 위한 압축본이다.

## Phase 1. 질문과 trace 범위를 먼저 세우기

- 당시 목표: `IP and ICMP Packet Analysis`를 어디서부터 읽어야 하는지 고정한다.
- 핵심 변경 단위: `study/03-Packet-Analysis-Top-Down/ip-icmp/problem/README.md`, `study/03-Packet-Analysis-Top-Down/ip-icmp/problem/Makefile`, `study/03-Packet-Analysis-Top-Down/ip-icmp/analysis/src/ip-icmp-analysis.md`
- 무슨 판단을 했는가: 처음엔 코드를 바로 읽기보다, 공개 진입점과 성공 기준부터 고정하는 편이 안전하다고 판단했다.
- 실행한 CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/ip-icmp/problem help
  open-traceroute        Open the traceroute trace in Wireshark GUI
  open-fragmentation     Open the fragmentation trace in Wireshark GUI
  filter-icmp            Show all ICMP packets from traceroute trace
  filter-fragments       Show fragmented IP packets
  filter-ttl             Show TTL values for ICMP echo requests
  summary                Print packet count summary for all traces
```
- 검증 신호:
  - `make help`만 봐도 이 프로젝트가 어떤 target으로 열리고 닫히는지 드러난다.
  - 이 단계에서의 역할: 전송 계층 랩 다음에 네트워크 계층 헤더와 제어 메시지를 직접 읽으며, 이후 `ICMP Pinger`와 `Traceroute` 구현 프로젝트와 맞물리게 합니다.
- 핵심 코드/trace 앵커: `study/03-Packet-Analysis-Top-Down/ip-icmp/analysis/src/ip-icmp-analysis.md`의 `## Part 1: IPv4 Header`
- 다음으로 넘어간 이유: 이제 어디를 읽어야 할지 정해졌으니, 실제로 판단이 몰린 함수나 trace section으로 내려갈 수 있었다.

## Phase 2. IPv4 header와 ICMP 흐름을 같은 분석 축으로 묶기

- 당시 목표: `IPv4 header, fragmentation, TTL, ICMP 메시지를 traceroute/ping 맥락에서 읽는 네트워크 계층 랩입니다.`를 실제 코드나 trace 근거에 붙여 본다.
- 핵심 변경 단위: `study/03-Packet-Analysis-Top-Down/ip-icmp/analysis/src/ip-icmp-analysis.md`
- 무슨 판단을 했는가: 핵심 설명은 한두 함수나 section에 가장 진하게 모여 있을 거라고 봤다.
- 실행한 CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/ip-icmp/problem filter-icmp
tshark -r data/ip-traceroute.pcapng -Y "icmp" -T fields \
5	10.0.0.2	93.184.216.34	3	8	0	0x0fa2
6	93.184.216.34	10.0.0.2	50	0	0	0x138b
```
- 검증 신호:
  - 이 출력만으로도 `## Part 2: IP Fragmentation` 주변이 설명의 중심축이라는 점이 드러난다.
  - fragmentation 3요소(`Identification`, `Flags`, `Offset`)
- 핵심 코드/trace 앵커: `study/03-Packet-Analysis-Top-Down/ip-icmp/analysis/src/ip-icmp-analysis.md`의 `## Part 2: IP Fragmentation`
- 다음으로 넘어간 이유: 중심 규칙을 잡은 뒤에는, 이 구현이나 분석이 실제로 무엇으로 닫히는지만 확인하면 됐다.

## Phase 3. verify 스크립트와 한계까지 정리하기

- 당시 목표: 통과 신호와 남은 범위를 한 번에 정리한다.
- 핵심 변경 단위: `study/03-Packet-Analysis-Top-Down/ip-icmp/analysis/src/ip-icmp-analysis.md`, `problem/script/`, `docs/`
- 무슨 판단을 했는가: 마지막에는 성공 신호와 한계를 같이 적어야 글이 매끈한 회고문으로 변하지 않는다고 판단했다.
- 실행한 CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/ip-icmp/problem test
PASS: ip-icmp answer file passed content verification
```
- 검증 신호:
  - `make -C study/03-Packet-Analysis-Top-Down/ip-icmp/problem test`가 현재 공개 답안을 다시 재현해 준다.
  - IPv4 중심이며 IPv6 비교는 개념 문서에서만 다룹니다.
- 핵심 코드/trace 앵커: `study/03-Packet-Analysis-Top-Down/ip-icmp/analysis/src/ip-icmp-analysis.md`의 `## Part 3: ICMP and Traceroute`
- 다음으로 넘어간 이유: 통과 신호와 경계가 모두 적혔으니, 긴 본문에서는 각 단계를 더 사람 읽기 좋게 풀어 쓰면 된다.
