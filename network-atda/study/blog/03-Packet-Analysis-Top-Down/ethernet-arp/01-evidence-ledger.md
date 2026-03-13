# Ethernet and ARP Packet Analysis evidence ledger

이 문서는 긴 본문을 읽기 전에, 세 단계에서 어떤 판단이 있었는지만 빠르게 붙들기 위한 압축본이다.

## Phase 1. 질문과 trace 범위를 먼저 세우기

- 당시 목표: `Ethernet and ARP Packet Analysis`를 어디서부터 읽어야 하는지 고정한다.
- 핵심 변경 단위: `study/03-Packet-Analysis-Top-Down/ethernet-arp/problem/README.md`, `study/03-Packet-Analysis-Top-Down/ethernet-arp/problem/Makefile`, `study/03-Packet-Analysis-Top-Down/ethernet-arp/analysis/src/ethernet-arp-analysis.md`
- 무슨 판단을 했는가: 문제 설명보다 실행 표면을 먼저 잡아야 뒤 설명이 흔들리지 않는다고 봤다.
- 실행한 CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/ethernet-arp/problem help
  open-trace             Open the ARP trace in Wireshark GUI
  filter-arp             Display all ARP packets via tshark
  filter-ethernet        Display Ethernet header info for first 20 packets
  filter-broadcast       Show broadcast frames
  summary                Print packet count summary
  verify                 Verify completeness of solve answers
```
- 검증 신호:
  - `make help`만 봐도 이 프로젝트가 어떤 target으로 열리고 닫히는지 드러난다.
  - 이 단계에서의 역할: 네트워크 계층 랩 다음에 링크 계층 주소 해석을 보며, 상위 계층 IP 주소와 하위 계층 MAC 주소가 어떻게 연결되는지 확인하게 합니다.
- 핵심 코드/trace 앵커: `study/03-Packet-Analysis-Top-Down/ethernet-arp/analysis/src/ethernet-arp-analysis.md`의 `## Part 1: Ethernet Frame Structure`
- 다음으로 넘어간 이유: 이제 어디를 읽어야 할지 정해졌으니, 실제로 판단이 몰린 함수나 trace section으로 내려갈 수 있었다.

## Phase 2. MAC 주소와 ARP 질의/응답을 한 시야로 붙들기

- 당시 목표: `링크 계층 프레임과 IP-MAC 주소 해석 과정을 ARP request/reply 쌍으로 읽는 랩입니다.`를 실제 코드나 trace 근거에 붙여 본다.
- 핵심 변경 단위: `study/03-Packet-Analysis-Top-Down/ethernet-arp/analysis/src/ethernet-arp-analysis.md`
- 무슨 판단을 했는가: 중심 규칙은 넓게 흩어져 있지 않고, 실제 분기나 frame evidence가 모이는 지점에 있다고 봤다.
- 실행한 CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/ethernet-arp/problem filter-arp
tshark -r data/ethernet-arp.pcapng -Y "arp" -T fields \
1	00:11:22:33:44:55	ff:ff:ff:ff:ff:ff	1	00:11:22:33:44:55	192.168.0.2	00:00:00:00:00:00	192.168.0.1
2	66:77:88:99:aa:bb	00:11:22:33:44:55	2	66:77:88:99:aa:bb	192.168.0.1	00:11:22:33:44:55	192.168.0.2
```
- 검증 신호:
  - 이 출력만으로도 `## Part 2: ARP Protocol` 주변이 설명의 중심축이라는 점이 드러난다.
  - ARP request broadcast / reply unicast
- 핵심 코드/trace 앵커: `study/03-Packet-Analysis-Top-Down/ethernet-arp/analysis/src/ethernet-arp-analysis.md`의 `## Part 2: ARP Protocol`
- 다음으로 넘어간 이유: 중심 규칙을 잡은 뒤에는, 이 구현이나 분석이 실제로 무엇으로 닫히는지만 확인하면 됐다.

## Phase 3. verify 스크립트와 한계까지 정리하기

- 당시 목표: 통과 신호와 남은 범위를 한 번에 정리한다.
- 핵심 변경 단위: `study/03-Packet-Analysis-Top-Down/ethernet-arp/analysis/src/ethernet-arp-analysis.md`, `problem/script/`, `docs/`
- 무슨 판단을 했는가: 검증 출력이 좋게 나와도 README limitation을 그대로 남겨야 범위가 정확해진다고 봤다.
- 실행한 CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/ethernet-arp/problem test
PASS: ethernet-arp answer file passed content verification
```
- 검증 신호:
  - `make -C study/03-Packet-Analysis-Top-Down/ethernet-arp/problem test`가 현재 공개 답안을 다시 재현해 준다.
  - trace가 작아 교재의 일부 확장 질문은 관찰 불가입니다.
- 핵심 코드/trace 앵커: `study/03-Packet-Analysis-Top-Down/ethernet-arp/analysis/src/ethernet-arp-analysis.md`의 `## Part 3: Broadcast and Caching`
- 다음으로 넘어간 이유: 통과 신호와 경계가 모두 적혔으니, 긴 본문에서는 각 단계를 더 사람 읽기 좋게 풀어 쓰면 된다.
