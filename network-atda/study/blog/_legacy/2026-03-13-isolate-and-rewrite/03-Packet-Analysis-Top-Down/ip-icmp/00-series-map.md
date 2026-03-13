# IP and ICMP Packet Analysis 시리즈 지도

## 이 프로젝트를 한 줄로

IP header 필드가 "교과서 정의"가 아니라 traceroute와 fragmentation 같은 실제 현상으로 어떻게 드러나는지 두 개의 trace로 묶어 보는 기록이다.

## 시작 전에 고정한 자료

- 제공 trace: `problem/data/ip-traceroute.pcapng`, `ip-fragmentation.pcapng`
- 실행 진입점: `problem/Makefile`
- 사용자 답안: `study/03-Packet-Analysis-Top-Down/ip-icmp/analysis/src/ip-icmp-analysis.md`
- 보조 개념 문서: `docs/concepts/wireshark-ip.md`

## 이 시리즈에서 따라갈 질문

1. traceroute trace에서 TTL 증가와 `ICMP Time Exceeded` 응답을 어떤 frame 쌍으로 읽어야 하는가.
2. `ip.id`, `flags`, `frag_offset`은 fragmentation을 설명할 때 어떻게 같이 써야 하는가.
3. Echo Request와 Echo Reply는 어떤 identifier/sequence 조합으로 매칭하는가.
4. reassembly가 어디서 일어나는지 trace evidence로 어디까지 말할 수 있는가.

## 검증 명령

- ICMP 전체: `make -C study/03-Packet-Analysis-Top-Down/ip-icmp/problem filter-icmp`
- TTL 증가 확인: `make -C study/03-Packet-Analysis-Top-Down/ip-icmp/problem filter-ttl`
- fragmentation 확인: `make -C study/03-Packet-Analysis-Top-Down/ip-icmp/problem filter-fragments`
- 답안 검증: `make -C study/03-Packet-Analysis-Top-Down/ip-icmp/problem test`

## 글 구성

| 파일 | 역할 |
| :--- | :--- |
| `00-series-map.md` | traceroute와 fragmentation을 한 프로젝트 안에서 어떻게 나눠 읽을지 정한다. |
| `10-development-timeline.md` | TTL 실험 → ICMP 응답 해석 → fragmentation/reassembly 순으로 이해를 쌓는다. |
