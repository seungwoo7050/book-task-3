# TCP and UDP Packet Analysis Blog

이 문서 묶음은 `tcp-udp` 랩을 "전송 계층 요약"이 아니라 "짧은 TCP upload trace와 2-packet UDP DNS trace를 같은 눈높이에서 읽으면 무엇이 stark하게 대비되는가"라는 질문으로 다시 읽는다. 현재 공개 답안은 TCP 쪽에서 3-way handshake, relative seq/ack, advertised window, data burst를 추적하고, UDP 쪽에서는 8-byte header와 length semantics를 최소 표면으로 확인한다. 따라서 이 lab의 핵심은 TCP 기능이 많다는 사실보다, 같은 전송 계층이라도 statefulness와 overhead가 얼마나 다르게 보이는지 직접 비교하는 데 있다.

이번 재작성은 기존 blog 본문이 아니라 다음 근거만 사용했다.

- 문제 정의: `study/03-Packet-Analysis-Top-Down/tcp-udp/problem/README.md`
- 답안 경계: `README.md`, `analysis/README.md`, `analysis/src/tcp-udp-analysis.md`
- 실제 검증: 2026-03-14 재실행한 `make -C network-atda/study/03-Packet-Analysis-Top-Down/tcp-udp/problem test`
- 보조 필터: `make -C .../tcp-udp/problem filter-handshake`, `filter-data`, `filter-udp`

## 읽는 순서

1. [`00-series-map.md`](./00-series-map.md)
2. [`10-development-timeline.md`](./10-development-timeline.md)
3. [`01-evidence-ledger.md`](./01-evidence-ledger.md)
4. [`02-structure.md`](./02-structure.md)

## 이번에 다시 확인한 검증 상태

- 정식 검증 명령: `make -C network-atda/study/03-Packet-Analysis-Top-Down/tcp-udp/problem test`
- 결과: `PASS: tcp-udp answer file passed content verification`
- 보조 필터에서 재확인한 값:
  - handshake frames `1/2/3`: `SYN -> SYN-ACK -> ACK`
  - client data seq progression: `1 -> 73 -> 273 -> ... -> 1073`
  - UDP query/reply: `192.168.0.2:55000 -> 8.8.4.4:53`, response length `62`

## 지금 남기는 한계

- TCP trace가 짧아서 teardown과 long-run congestion avoidance 전환은 직접 보이지 않는다.
- retransmission이 없는 clean trace라 loss recovery 장면은 학습할 수 없다.
- UDP 쪽도 2 packet DNS 예시뿐이라 jitter나 reordering 같은 성질은 보이지 않는다.
