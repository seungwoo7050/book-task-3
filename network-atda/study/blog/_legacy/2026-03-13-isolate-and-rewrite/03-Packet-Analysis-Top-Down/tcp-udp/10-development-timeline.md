# TCP and UDP Packet Analysis 개발 타임라인

## Day 1 — TCP를 먼저 읽고, UDP를 비교 대상으로 붙이기

### Session 1

- 목표: TCP trace에서 연결이 시작되는 최소 골격을 먼저 잡는다.
- 진행: `filter-handshake`부터 실행해서 SYN, SYN-ACK, 마지막 ACK를 분리했다. 그다음 frame 15의 HTTP POST가 handshake 이후 어느 sequence에서 시작되는지 확인했다.
- 이슈: 처음에는 `POST /upload` frame이 제일 중요해 보였다. 하지만 데이터 양이나 RTT를 계산하려면 그 전에 연결이 어떻게 성립했는지를 알아야 했다. 결국 frame 15만 읽는 방식은 너무 늦은 출발이었다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem filter-handshake
1   192.168.0.2      128.119.245.12   54000   80   0x0002   0      0
2   128.119.245.12   192.168.0.2      80      54000 0x0012   0      1
3   192.168.0.2      128.119.245.12   54000   80   0x0010   1      1
```

- 메모: 상대 sequence 번호를 쓰는 trace라 숫자가 작아서 오히려 흐름이 잘 보였다. `0 -> 0/1 -> 1/1` 패턴을 먼저 잡아 두니 이후 ACK 계산이 쉬워졌다.

### Session 2

- 목표: 데이터 구간에서 sequence, ack, payload, receiver window를 읽는다.
- 진행: `filter-data` 출력으로 client data-bearing segment를 나열했다. frame 4의 72바이트를 시작으로 200바이트 segment들이 이어지고, server ACK가 누적되며 `ack=273`, `473`, `673`처럼 올라간다. 여기서 RTT도 대략 0.19ms 수준으로 계산했다.
- 이슈: 처음엔 frame 15의 POST만 보면 총 전송량도 바로 알 수 있을 거라 생각했다. 실제로는 첫 data frame부터 마지막 ACK까지 전부 이어서 봐야 1272바이트라는 총량이 자연스럽게 계산됐다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem filter-data
4    1      1      72    64240
5    73     1      200   64240
7    273    1      200   64240
9    473    1      200   64240
11   673    1      200   64240
13   873    1      200   64240
15   1073   1      200   64240
```

- 메모: 짧은 trace인데도 ACK가 누적되는 모습은 분명했다. 이 구간을 보고 나서야 TCP를 "상태를 계속 쌓는 프로토콜"로 체감했다.

### Session 3

- 목표: 보이지 않는 것과 보이는 것을 정확히 나눈다.
- 진행: retransmission 필터를 돌렸더니 아무것도 나오지 않았다. 이건 "이번 trace에서는 재전송이 관찰되지 않는다"는 뜻이지, TCP가 언제나 깔끔하게 동작한다는 뜻은 아니다. 이어서 UDP trace를 열어 TCP와 비교했다.
- 이슈: 짧은 trace라 congestion window 변화나 connection teardown 같은 이야기를 하고 싶었지만, 실제 frame이 없었다. 그런 내용을 일반론으로 채우는 순간 이 글은 trace 분석이 아니라 강의 요약이 된다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem filter-retransmissions
```

```bash
$ make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem filter-udp
1   192.168.0.2      8.8.8.8         53000   53   36
2   8.8.8.8          192.168.0.2     53      53000 52
```

```bash
$ make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem test
bash script/verify_answers.sh
TCP/UDP analysis answers look complete.
```

- 정리:
	- TCP는 handshake와 누적 ACK를 먼저 읽어야 데이터 설명이 맞아떨어졌다.
	- retransmission 필터가 비어 있다는 사실 자체도 중요한 evidence였다.
	- teardown, cwnd 전개처럼 trace가 보여 주지 않는 것은 끝까지 `관찰 불가`로 남겨야 했다.
	- UDP는 두 packet만으로도 header 4개 필드와 `ip.proto=17` 비교를 설명하기에 충분했다.
