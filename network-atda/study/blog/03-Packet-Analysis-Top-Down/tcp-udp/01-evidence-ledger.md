# TCP and UDP Packet Analysis Evidence Ledger

## 이번에 읽은 자료

- 문제 사양: `study/03-Packet-Analysis-Top-Down/tcp-udp/problem/README.md`
- 답안 엔트리: `study/03-Packet-Analysis-Top-Down/tcp-udp/analysis/src/tcp-udp-analysis.md`
- 검증 스크립트: `study/03-Packet-Analysis-Top-Down/tcp-udp/problem/script/verify_answers.sh`
- 실행 표면: `study/03-Packet-Analysis-Top-Down/tcp-udp/problem/Makefile`

## 핵심 근거

- `filter-handshake` 출력:
  - frame `1` client SYN `seq=0`
  - frame `2` server SYN-ACK `seq=0 ack=1`
  - frame `3` client ACK `seq=1 ack=1`
- `filter-data` 출력:
  - frame `4` `seq=1 len=72`
  - frames `5/7/9/11/13/15`는 `200-byte` payload
- `analysis/src/tcp-udp-analysis.md`:
  - total client bytes `1272`
  - RTT samples around `0.19-0.21 ms`
  - no `FIN`, no retransmission, no clear cwnd phase transition
- `filter-udp` 출력:
  - frame `1` `55000 -> 53` length `36`
  - frame `2` `53 -> 55000` length `62`

## 테스트 근거

`make -C network-atda/study/03-Packet-Analysis-Top-Down/tcp-udp/problem test`

결과:

- `PASS: tcp-udp answer file passed content verification`

## 이번에 고정한 해석

- TCP 쪽 핵심은 POST payload 내용보다 connection state가 단계적으로 눈에 드러난다는 점이다.
- clean trace라 retransmission과 long congestion story는 못 보지만, handshake와 ACK만으로도 TCP의 statefulness는 충분히 선명하다.
- UDP 쪽은 정보가 적어서 덜 중요한 것이 아니라, protocol contract 자체가 deliberately 작다는 점이 중요하다.
