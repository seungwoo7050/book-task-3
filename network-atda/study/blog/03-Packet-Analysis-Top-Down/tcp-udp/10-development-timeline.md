# TCP and UDP Packet Analysis development timeline

`TCP and UDP Packet Analysis`는 결과만 보면 단순해 보이지만, 실제로는 어느 파일에서 규칙을 고정했는지 따라가야 전체 그림이 보인다.

아래 순서는 README 설명을 다시 요약한 것이 아니라, 실제 근거가 남아 있는 지점을 따라 재조립한 흐름이다.

## 구현 순서 한눈에 보기

1. `study/03-Packet-Analysis-Top-Down/tcp-udp/problem`의 문제 문서와 실행 target으로 출발점을 고정했다.
2. `study/03-Packet-Analysis-Top-Down/tcp-udp/analysis/src/tcp-udp-analysis.md`의 핵심 구간에서 동작 규칙을 설명할 수 있는 최소 앵커를 골랐다.
3. `make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem test`와 테스트/verify 파일을 연결해 통과 신호와 남은 경계를 정리했다.

## 1. 질문과 trace 범위를 먼저 세우기

출발점에서 중요한 건 기능 목록이 아니라 읽는 순서였다. `problem/` 문서와 Makefile만으로도 첫 발을 어디에 둘지 정리할 수 있었다.

- 당시 목표: `TCP and UDP Packet Analysis`를 읽는 출발점과 성공 기준을 고정한다.
- 실제 진행: `problem/README.md`와 `problem/Makefile`을 먼저 확인한 뒤, `## Part 1: TCP Segment Structure`가 있는 파일로 내려갔다.
- 검증 신호: `make help`에 보이는 target만으로도 이 프로젝트가 어떤 명령으로 열리고 닫히는지 설명할 수 있었다.
- 새로 배운 것: 3-way handshake 해석

핵심 코드/trace:

```text
## Part 1: TCP Segment Structure

**Trace file**: `tcp-upload.pcapng`

### Question 1

**Q: What client/server IP and port are used?**
```

왜 이 코드가 중요했는가:

첫 단계에서 이 코드를 붙드는 편이 좋은 이유는, 뒤 단계 전체가 여기서 정한 입력과 실행 방식 위에 쌓이기 때문이다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem help
  open-tcp               Open the TCP upload trace in Wireshark GUI
  open-udp               Open the UDP DNS trace in Wireshark GUI
  filter-handshake       Show the TCP 3-way handshake (SYN, SYN-ACK, ACK)
  filter-data            Show TCP data segments (payload > 0)
  filter-retransmissions Show TCP retransmissions
  filter-udp             Show all UDP packets from DNS trace
```

## 2. handshake와 data segment를 비교 가능한 근거로 정리하기

두 번째 단계에서는 `TCP의 신뢰성 메커니즘과 UDP의 단순성을 같은 전송 계층 시야에서 비교하는 랩입니다.`라는 설명을 실제 코드나 trace 근거에 붙여야 했다. 그래서 파일 전체를 훑기보다 판단이 몰린 구간 하나를 먼저 골랐다.

- 당시 목표: `TCP의 신뢰성 메커니즘과 UDP의 단순성을 같은 전송 계층 시야에서 비교하는 랩입니다.`를 실제 근거에 붙인다.
- 실제 진행: `## Part 2: TCP Connection Management` 주변을 중심으로 symbol이나 trace 결과를 다시 좁혀 읽었다.
- 검증 신호: 짧은 `rg`/filter 출력만으로도 어느 줄이 설명의 중심인지 바로 드러났다.
- 새로 배운 것: relative sequence/ack 읽기

핵심 코드/trace:

```text
## Part 2: TCP Connection Management

### Question 6

**Q: Minimum receiver window? Does it reach zero?**

**A:** Minimum advertised window from server packets is **8192** bytes (SYN-ACK). During data transfer, server advertises **64240** and never reaches zero.
```

왜 이 코드가 중요했는가:

이 스니펫은 실제 판단이 몰린 줄을 보여 준다. 설명을 길게 하기보다 이 줄을 기준으로 앞뒤 규칙을 읽는 편이 빠르다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem filter-handshake
tshark -r data/tcp-upload.pcapng -Y "tcp.flags.syn == 1 || (tcp.flags.ack == 1 && tcp.seq == 1 && tcp.ack == 1)" \
3	192.168.0.2	128.119.245.12	54000	80	0x0010	1	1
4	192.168.0.2	128.119.245.12	54000	80	0x0018	1	1
```

## 3. verify 스크립트와 한계까지 정리하기

검증 단계에서는 결과보다 계약을 봤다. 어떤 출력이 통과 신호인지, 그리고 README에 남겨 둔 한계가 무엇인지 함께 정리했다.

- 당시 목표: 검증 결과와 남은 경계를 함께 정리한다.
- 실제 진행: `make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem test`를 다시 실행하고, `## Part 3: UDP`가 남아 있는 파일을 본문 마지막 근거로 삼았다.
- 검증 신호: 현재 공개 답안이 재현된다는 출력과, README limitation이 동시에 확인됐다.
- 새로 배운 것: window field와 retransmission 표시

핵심 코드/trace:

```text
# TCP & UDP Lab — Analysis Answers

## Trace Limitations

- This report uses only the repository-provided trace files.
- If a worksheet item needs packets that are not present in these traces, the answer is marked as `Not observable in this provided trace`.
- Missing values are not guessed; only decoded packet evidence is used.
- Numeric claims are tied to explicit frame references.
```

왜 이 코드가 중요했는가:

본문을 여기로 닫으면 구현 설명이 감상문으로 흘러가지 않는다. 어떤 계약을 확인했는지 바로 보이기 때문이다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem test
PASS: tcp-udp answer file passed content verification
```

## 남은 경계

- trace가 짧아 전체 congestion window evolution을 직접 보기는 어렵습니다.
- teardown과 장기 혼잡 제어 관찰은 제한적입니다.
