# 802.11 Wireless Packet Analysis 시리즈 지도

## 이 프로젝트를 한 줄로

무선 LAN 연결을 복잡한 용어 목록이 아니라 beacon부터 data/ACK까지 이어지는 짧은 절차로 복원해 보는 기록이다.

## 시작 전에 고정한 자료

- 제공 trace: `problem/data/wireless-trace.pcap`
- 실행 진입점: `problem/Makefile`
- 사용자 답안: `study/03-Packet-Analysis-Top-Down/wireless-802.11/analysis/src/wireless-analysis.md`
- 보조 개념 문서: `docs/concepts/wireshark-wireless.md`

## 이 시리즈에서 따라갈 질문

1. beacon과 probe response는 같은 AP 정보를 어떻게 다른 맥락에서 보여 주는가.
2. authentication과 association는 어떤 frame 순서로 이어져야 연결이 성립했다고 말할 수 있는가.
3. `To DS`, `From DS`, AID, ACK frame은 연결 이후 데이터 전송을 어떻게 보여 주는가.
4. synthetic trace의 단순화는 capability, security detail, data exchange 양에서 어디서 드러나는가.

## 검증 명령

- beacon 확인: `make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem beacons`
- probe 확인: `make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem probes`
- authentication: `make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem auth`
- association: `make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem assoc`
- data frame: `make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem data`
- 답안 검증: `make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem test`

## 글 구성

| 파일 | 역할 |
| :--- | :--- |
| `00-series-map.md` | management frame sequence를 먼저 정리한다. |
| `10-development-timeline.md` | beacon/probe → auth/assoc → data/ACK 순서로 연결 절차를 따라간다. |
