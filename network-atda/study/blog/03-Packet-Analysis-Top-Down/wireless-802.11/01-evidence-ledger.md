# 802.11 Wireless Packet Analysis evidence ledger

이 문서는 긴 본문을 읽기 전에, 세 단계에서 어떤 판단이 있었는지만 빠르게 붙들기 위한 압축본이다.

## Phase 1. 질문과 trace 범위를 먼저 세우기

- 당시 목표: `802.11 Wireless Packet Analysis`를 어디서부터 읽어야 하는지 고정한다.
- 핵심 변경 단위: `study/03-Packet-Analysis-Top-Down/wireless-802.11/problem/README.md`, `study/03-Packet-Analysis-Top-Down/wireless-802.11/problem/Makefile`, `study/03-Packet-Analysis-Top-Down/wireless-802.11/analysis/src/wireless-analysis.md`
- 무슨 판단을 했는가: 처음엔 코드를 바로 읽기보다, 공개 진입점과 성공 기준부터 고정하는 편이 안전하다고 판단했다.
- 실행한 CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem help
  open            - Open trace file in Wireshark
  beacons         - Filter beacon frames
  probes          - Filter probe request/response frames
  auth            - Filter authentication frames
  assoc           - Filter association request/response frames
  data            - Filter 802.11 data frames
```
- 검증 신호:
  - `make help`만 봐도 이 프로젝트가 어떤 target으로 열리고 닫히는지 드러난다.
  - 이 단계에서의 역할: Ethernet/ARP 다음에 무선 링크 계층의 차이를 관찰하며, 같은 링크 계층이라도 프레임 구조와 주소 의미가 크게 달라짐을 보여 줍니다.
- 핵심 코드/trace 앵커: `study/03-Packet-Analysis-Top-Down/wireless-802.11/analysis/src/wireless-analysis.md`의 `## Part 1: Beacon Frames (Q1–Q5)`
- 다음으로 넘어간 이유: 이제 어디를 읽어야 할지 정해졌으니, 실제로 판단이 몰린 함수나 trace section으로 내려갈 수 있었다.

## Phase 2. beacon과 probe 이후 association 흐름을 이어 읽기

- 당시 목표: `비콘, 프로브, 인증, 연관, 주소 필드를 통해 무선 LAN 연결 과정을 읽는 랩입니다.`를 실제 코드나 trace 근거에 붙여 본다.
- 핵심 변경 단위: `study/03-Packet-Analysis-Top-Down/wireless-802.11/analysis/src/wireless-analysis.md`
- 무슨 판단을 했는가: 핵심 설명은 한두 함수나 section에 가장 진하게 모여 있을 거라고 봤다.
- 실행한 CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem beacons
tshark -r data/wireless-trace.pcap -Y "wlan.fc.type_subtype == 0x08" \
1	00:16:b6:f7:1d:51	3330204d756e726f65205374	100
2	00:16:b6:f7:1d:52	6c696e6b7379733132	100
```
- 검증 신호:
  - 이 출력만으로도 `## Part 2: Probe Request and Response (Q6–Q9)` 주변이 설명의 중심축이라는 점이 드러난다.
  - beacon과 probe의 의미
- 핵심 코드/trace 앵커: `study/03-Packet-Analysis-Top-Down/wireless-802.11/analysis/src/wireless-analysis.md`의 `## Part 2: Probe Request and Response (Q6–Q9)`
- 다음으로 넘어간 이유: 중심 규칙을 잡은 뒤에는, 이 구현이나 분석이 실제로 무엇으로 닫히는지만 확인하면 됐다.

## Phase 3. verify 스크립트와 한계까지 정리하기

- 당시 목표: 통과 신호와 남은 범위를 한 번에 정리한다.
- 핵심 변경 단위: `study/03-Packet-Analysis-Top-Down/wireless-802.11/analysis/src/wireless-analysis.md`, `problem/script/`, `docs/`
- 무슨 판단을 했는가: 마지막에는 성공 신호와 한계를 같이 적어야 글이 매끈한 회고문으로 변하지 않는다고 판단했다.
- 실행한 CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem test
PASS: wireless-802.11 answer file passed content verification
```
- 검증 신호:
  - `make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem test`가 현재 공개 답안을 다시 재현해 준다.
  - compact synthetic trace라 실제 monitor-mode 캡처보다 단순화된 부분이 있습니다.
- 핵심 코드/trace 앵커: `study/03-Packet-Analysis-Top-Down/wireless-802.11/analysis/src/wireless-analysis.md`의 `## Part 3: Authentication and Association (Q10–Q14)`
- 다음으로 넘어간 이유: 통과 신호와 경계가 모두 적혔으니, 긴 본문에서는 각 단계를 더 사람 읽기 좋게 풀어 쓰면 된다.
