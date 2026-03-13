# TCP and UDP Packet Analysis 시리즈 지도

## 이 프로젝트를 한 줄로

TCP의 상태fulness와 UDP의 단순함을 한 번에 비교하되, 짧은 trace가 허용하는 주장과 허용하지 않는 주장을 구분해 보는 기록이다.

## 시작 전에 고정한 자료

- 제공 trace: `problem/data/tcp-upload.pcapng`, `udp-dns.pcapng`
- 실행 진입점: `problem/Makefile`
- 사용자 답안: `study/03-Packet-Analysis-Top-Down/tcp-udp/analysis/src/tcp-udp-analysis.md`
- 보조 문서: `docs/concepts/reproducibility.md`

## 이 시리즈에서 따라갈 질문

1. TCP 3-way handshake와 첫 데이터 전송 구간을 어떤 frame 묶음으로 읽어야 하는가.
2. 짧은 TCP trace에서 sequence, ack, receiver window, RTT는 어디까지 계산할 수 있는가.
3. `tcp.analysis.retransmission`이 비어 있을 때, 무엇을 "없다"고 말할 수 있고 무엇은 여전히 모른다고 남겨야 하는가.
4. UDP trace는 왜 packet 두 개만으로도 header 구조와 protocol number 비교에 충분한가.

## 검증 명령

- handshake: `make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem filter-handshake`
- data segments: `make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem filter-data`
- retransmission 확인: `make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem filter-retransmissions`
- UDP 비교: `make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem filter-udp`
- 답안 검증: `make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem test`

## 글 구성

| 파일 | 역할 |
| :--- | :--- |
| `00-series-map.md` | TCP와 UDP를 어떤 순서로 비교할지 미리 고정한다. |
| `10-development-timeline.md` | handshake → data/ACK 흐름 → retransmission 부재 → UDP 비교 순으로 관찰을 쌓는다. |
