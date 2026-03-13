# 802.11 Wireless Packet Analysis development timeline

`802.11 Wireless Packet Analysis`의 핵심은 완성 결과보다, 어떤 순서로 범위를 좁히고 검증까지 닫았는가에 있다.

본문은 코드나 trace를 한 번에 길게 복붙하지 않고, 판단이 바뀐 지점만 골라 이어 붙인다.

## 구현 순서 한눈에 보기

1. `study/03-Packet-Analysis-Top-Down/wireless-802.11/problem`의 문제 문서와 실행 target으로 출발점을 고정했다.
2. `study/03-Packet-Analysis-Top-Down/wireless-802.11/analysis/src/wireless-analysis.md`의 핵심 구간에서 동작 규칙을 설명할 수 있는 최소 앵커를 골랐다.
3. `make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem test`와 테스트/verify 파일을 연결해 통과 신호와 남은 경계를 정리했다.

## 1. 질문과 trace 범위를 먼저 세우기

처음에는 `802.11 Wireless Packet Analysis`를 어디서부터 설명해야 할지부터 정리해야 했다. 그래서 문제 문서와 `make help` 출력으로 공개된 실행 표면을 먼저 잡았다.

- 당시 목표: `802.11 Wireless Packet Analysis`를 읽는 출발점과 성공 기준을 고정한다.
- 실제 진행: `problem/README.md`와 `problem/Makefile`을 먼저 확인한 뒤, `## Part 1: Beacon Frames (Q1–Q5)`가 있는 파일로 내려갔다.
- 검증 신호: `make help`에 보이는 target만으로도 이 프로젝트가 어떤 명령으로 열리고 닫히는지 설명할 수 있었다.
- 새로 배운 것: management/control/data frame 분류

핵심 코드/trace:

```text
## Part 1: Beacon Frames (Q1–Q5)

### Q1. SSIDs of Access Points Issuing Beacon Frames

Unique SSIDs observed in beacon frames:
- **30 Munroe St** (frame #1)
- **linksys12** (frame #2)
```

왜 이 코드가 중요했는가:

이 부분을 먼저 보여 주는 이유는, 이 프로젝트의 진입점과 실행 표면이 여기서 한 번에 정리되기 때문이다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem help
  open            - Open trace file in Wireshark
  beacons         - Filter beacon frames
  probes          - Filter probe request/response frames
  auth            - Filter authentication frames
  assoc           - Filter association request/response frames
  data            - Filter 802.11 data frames
```

## 2. beacon과 probe 이후 association 흐름을 이어 읽기

이제부터는 설명을 추상적으로 유지할 수 없었다. 실제 분기나 frame evidence가 모이는 지점을 찾아야 글이 살아났다.

- 당시 목표: `비콘, 프로브, 인증, 연관, 주소 필드를 통해 무선 LAN 연결 과정을 읽는 랩입니다.`를 실제 근거에 붙인다.
- 실제 진행: `## Part 2: Probe Request and Response (Q6–Q9)` 주변을 중심으로 symbol이나 trace 결과를 다시 좁혀 읽었다.
- 검증 신호: 짧은 `rg`/filter 출력만으로도 어느 줄이 설명의 중심인지 바로 드러났다.
- 새로 배운 것: beacon과 probe의 의미

핵심 코드/trace:

```text
## Part 2: Probe Request and Response (Q6–Q9)

### Q6. Probe Request Source and SSID

Probe Request is frame **#3**:
- Source MAC: **00:12:f0:1c:3e:82**
- SSID: **30 Munroe St**
```

왜 이 코드가 중요했는가:

여기서는 구현이나 분석의 무게중심이 바뀐다. 그래서 파일 전체보다 이 좁은 구간을 먼저 보는 편이 훨씬 정확하다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem beacons
tshark -r data/wireless-trace.pcap -Y "wlan.fc.type_subtype == 0x08" \
1	00:16:b6:f7:1d:51	3330204d756e726f65205374	100
2	00:16:b6:f7:1d:52	6c696e6b7379733132	100
```

## 3. verify 스크립트와 한계까지 정리하기

끝맺음에서 중요한 건 멋진 회고가 아니라 경계선이다. 통과한 범위와 남겨 둔 범위를 같은 문맥 안에 두려고 했다.

- 당시 목표: 검증 결과와 남은 경계를 함께 정리한다.
- 실제 진행: `make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem test`를 다시 실행하고, `## Part 3: Authentication and Association (Q10–Q14)`가 남아 있는 파일을 본문 마지막 근거로 삼았다.
- 검증 신호: 현재 공개 답안이 재현된다는 출력과, README limitation이 동시에 확인됐다.
- 새로 배운 것: authentication -> association 절차

핵심 코드/trace:

```text
## Part 3: Authentication and Association (Q10–Q14)

### Q10. Authentication Algorithm

Authentication frames (#5 and #6) use **Open System** algorithm (`Authentication Algorithm: 0`).

### Q11. Auth Request Addresses and Auth Response Status
```

왜 이 코드가 중요했는가:

최종 단계에서 중요한 것은 '잘 됐다'가 아니라 '무엇을 확인했고 무엇은 아직 안 했다'인데, 그 기준이 이 파일에 가장 잘 남아 있다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem test
PASS: wireless-802.11 answer file passed content verification
```

## 남은 경계

- compact synthetic trace라 실제 monitor-mode 캡처보다 단순화된 부분이 있습니다.
- EAPOL/WPA handshake 심화는 포함하지 않습니다.
- 실제 RF 잡음과 retry 패턴은 제한적으로만 보입니다.
